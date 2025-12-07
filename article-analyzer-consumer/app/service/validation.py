import os
import json
import google.generativeai as genai
from typing import List
from app.core.config import settings


# --- Load Prompt Files ---
def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

script_dir = os.path.dirname(os.path.realpath(__file__))
app_dir = os.path.dirname(script_dir)
prompts_dir = os.path.join(app_dir, 'prompts')

prompt_path = os.path.join(prompts_dir, 'eval_model_prompt.txt')
evaluation_prompt_path = os.path.join(prompts_dir, 'evaluation_prompt.txt')
output_path = os.path.join(prompts_dir, 'control_output.json') 

PROMPT = load_prompt(prompt_path)  # For base extraction
EVALUATION_PROMPT = load_prompt(evaluation_prompt_path)  # For scoring

# --- Configure Gemini ---
# IMPORTANT: Add your personal Google Gemini API key in the .env file before running this code
class Evaluation:
    def __init__(self):
        genai.configure(api_key=settings.app.API_KEY)
        self.model = genai.GenerativeModel(settings.validation.MODEL_NAME)
        self.temperature = settings.validation.TEMPERATURE
        self.top_p = settings.validation.TOP_P
        self.top_k = settings.validation.TOP_K

    # --- Step 1: Generate base prompt output only ---
    def transform_to_evaluation_format(self, gemini_output: dict) -> List[dict]:
        output = []
        for i in gemini_output['extraction_details']:
            temp_json = {
                'attribution': i['attribution'],
                'attribution_type': i['attribution_type'],
                'designation': i['designation'],
                'comments': [elem['comment'] for elem in i['comment_details']]
            }
            output.append(temp_json)
        return output
    
    def get_prompt_based_result(self,article: str) -> List[dict]:
        prompt_response = self.model.generate_content(
            PROMPT + "\n" + article,
            generation_config={
                'temperature':0,
                'top_p':1,
                'top_k':1
            }
        )
        result_1 = prompt_response.text.strip("```json").strip("```")
        return json.loads(result_1)

    # --- Step 2: Evaluate against provided Pydantic result ---
    def evaluate(self,article: str, model_output: dict) -> dict:
        base_result = self.get_prompt_based_result(article)
        transformed_pydantic = self.transform_to_evaluation_format(model_output)

        eval_input = (
            f"{EVALUATION_PROMPT.strip()}\n\n"
            f"Base Prompt Results: {json.dumps(base_result, indent=2)}\n\n"
            f"Pydantic Results: {json.dumps(transformed_pydantic, indent=2)}"
        )

        eval_response = self.model.generate_content(eval_input)
        result_text = eval_response.text
        cleaned_text = result_text.strip().strip("```json").strip("```").strip()
        print(cleaned_text)
        eval_data = json.loads(cleaned_text)
        full_evaluation_text = eval_data.get("full_evaluation_text")
        accuracy_score_10 = eval_data.get("accuracy_score_10")
        return full_evaluation_text, float(accuracy_score_10)