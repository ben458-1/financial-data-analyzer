import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.db.fetching_article import fetch_full_article_json
from app.service.search import search_articles_by_nl_query
from app.logger import log

app = FastAPI(
    title="Article Search App",
    description="Search articles by people, spokespersons, organizations, etc. using natural language."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class ArticleDetailsRequest(BaseModel):
    article_id: int


@app.post("/query")
async def query_articles(query: QueryRequest):
    try:
        search_output = await search_articles_by_nl_query(query.query) 
        return search_output
    except Exception as e:
        log.log_error(f"Error searching for article in db. Error:{e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/article")
async def fetch_entire_article_details(request: ArticleDetailsRequest):
    try:
        spokesperson_details, source_details, article_info, people_info, author_info  = fetch_full_article_json(request.article_id)
        log.log_info("Response payload successfully received")
        return{
            "article": article_info, #dictionary
            "author": author_info,  #dictionary
            "people_info": people_info,  #list of dictionaries
            "spokesperson": spokesperson_details, #list of dictionaries
            "source": source_details #list of dictionaries
        }
    except Exception as e:
        log.log_error(f"Error fetching data from the db. Error:{e}")    
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
async def root():
    return {"message": "Welcome to the Fetchin Module. Use the /query endpoint."}


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)