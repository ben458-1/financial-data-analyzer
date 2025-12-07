import os
import sys
import json
from google import genai
from pydantic import BaseModel, Field
from app.prompts.prmt_framework import Comment_Extraction
from app.core.config import settings
from app.logger import log

def read_input_file(filename: str) -> str:
    """Reads the content of a file located in the same directory as the script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(script_dir) # This goes from 'services' to 'app'
    prompts_dir = os.path.join(app_dir, 'prompts')
    file_path = os.path.join(prompts_dir, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        log.log_info("Successfully read prompt from file")
        return content
    except FileNotFoundError:
        log.log_error(f"Error: Input file not found at '{file_path}'")
        sys.exit(1) # Exit the script if the file is not found
    except IOError as e:
        log.log_error(f"Error reading file '{file_path}': {e}")
        sys.exit(1) # Exit on other read errors
    except Exception as e:
        log.log_error(f"An unexpected error occurred while reading the file: {e}")
        sys.exit(1)    

class ResponseHandlerConfig(BaseModel):
    model_name: str = Field(settings.parsing.MODEL_NAME, description="Model name for generation")
    max_output_tokens: int = Field(settings.parsing.MAX_OUTPUT_TOKENS, description="Maximum output tokens", ge=1)
    temperature: float = Field(settings.parsing.TEMPERATURE, description="Temperature for generation", ge=0, le=1)
    top_p: float = Field(settings.parsing.TOP_P, description="Top-p for generation", ge=0, le=1)
    top_k: int = Field(settings.parsing.TOP_K, description="Top-k for generation", ge=1)
    candidate_count: int = Field(settings.parsing.CANDIDATE_COUNT, description="Number of candidate responses", ge=1)


custom_prompt_default = read_input_file("prompt.txt")

class ResponseHandler:
    
    api_key_index: int = 0
    
    def __init__(self, resp_config: ResponseHandlerConfig = None, custom_prompt: str = custom_prompt_default):
        if resp_config is None:
            resp_config = ResponseHandlerConfig(**settings.parsing.model_dump())
        # IMPORTANT: Add your personal Google Gemini API key in the .env file before running this code
        self.api_key = settings.app.API_KEY
        if not self.api_key:
            log.log_info("API key not found")
            raise ValueError("API key not found in environment variables. Please add your Google Gemini API key to the .env file.")

        self.client = genai.Client(api_key=self.api_key)
        self.model = resp_config.model_name
        self.max_output_tokens = resp_config.max_output_tokens
        self.temperature = resp_config.temperature
        self.top_p = resp_config.top_p
        self.top_k = resp_config.top_k
        self.candidate_count = resp_config.candidate_count
        self.extraction_structure = Comment_Extraction
        self._custom_prompt = custom_prompt
        
    @property
    def custom_prompt(self):
        return self._custom_prompt
        
    def extraction(self, input_content: str, index):
        try:
            response = self.client.models.generate_content(
                model = self.model,
                contents= self.custom_prompt + input_content,
                config={
                    'response_mime_type': 'application/json',
                    'response_schema': self.extraction_structure,
                    'max_output_tokens': self.max_output_tokens,
                    'temperature': self.temperature,
                    'top_p': self.top_p,
                    'top_k':self.top_k,
                    "candidate_count":self.candidate_count
                },
            )
            # if response.get("status", "") == 'RESOURCE_EXHAUSTED':
            #     self.switch_key()
            #     if index >= 5:
            #         return self.extraction(input_content, index + 1)
            #     else:
            #         return None
            log.log_info("Article analyzed, parsed and output json received from the model ")
            response_data = json.loads(response.text)
            pretty_output = json.dumps(response_data, indent=4)
            
            return response.text

        except Exception as e:
            log.log_warning("Gemini Resource Exhausted")
            if 'RESOURCE_EXHAUSTED' in str(e) or 'quota' in str(e).lower():
                self.switch_key()
                if index <= 5:
                    return self.extraction(input_content, index + 1)
                else:
                    return None
            else:
                log.log_error(f"An error occurred: {e}")
            return None
        
    def switch_key(self):
        self.api_key_index = self.api_key_index + 1
        keys = settings.app.API_KEYS
        if len(keys) > self.api_key_index:
            log.log_warning(f"Quota exhausted for {len(keys)} API key(s). Attempting to switch to the next available key.")
            self.api_key = keys[self.api_key_index]
            settings.app.API_KEY = self.api_key
            self.client = genai.Client(api_key=self.api_key)
        else:
            log.log_error("All configured API keys are exhausted. No further requests can be processed until quota resets or new keys are added.")
            self.api_key_index = 0
            self.api_key = settings.app.api_key_itr(self.api_key_index)
            self.client = genai.Client(api_key=self.api_key)