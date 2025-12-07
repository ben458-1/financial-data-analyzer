from typing import List, Dict, Any
import psycopg2
import asyncio
import google.generativeai as genai
from fastapi import HTTPException
from app.core.config import settings

# -- DB Config --
DB_PARAMS = {
    "host": settings.db.HOST,
    "port": settings.db.PORT,
    "database": settings.db.NAME,
    "user": settings.db.USER,
    "password": settings.db.PASSWORD
}

# --- UTILS ---
def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)


def get_database_schema(cursor):
    # cursor.execute("""
    #     SELECT table_name 
    #     FROM information_schema.tables 
    #     WHERE table_schema = 'ai'
    # """)
    # tables = cursor.fetchall()
    schema_info = """
Table: spokesperson_details
- spokesperson_id (serial, primary key)
- article_id (int, not null)
- name (varchar)
- designation (varchar)
- organization (varchar)
- spk_place_location (varchar)
- spk_place_state (varchar)
- spk_place_country (varchar)
- people_in_comments (text)
- competitors_mentioned (text)
- spk_past_designation (varchar)
- spk_past_organization (varchar)
- spk_past_no_of_years (int)
- spk_past_time_period (varchar)
- spk_past_location (varchar)
- spk_past_country (varchar)
- spk_summary (text)
- comment_date (jsonb)

Table: source_details
- source_id (serial, primary key)
- article_id (int, not null)
- designation (varchar)
- organization (varchar)
- people_in_comments (text)
- competitors_mentioned (text)
- comment_date (jsonb)

Table: comment_details
- comment_id (serial, primary key)
- spokesperson_id (int, foreign key to spokesperson_details.spokesperson_id, nullable)
- source_id (int, foreign key to source_details.source_id, nullable)
- comment (varchar)
- reference_type (varchar)
- from_to (text)
- comment_keywords (text)
- stk_in_the_com (text)

Table: article_details
- id (serial, primary key)
- article_id (int, not null)
- newspaper_id (int, not null)
- header (varchar)
- link_to_article (varchar)
- article_keywords (text)
- author_name (varchar)
- author_comments (text)
- author_designation (jsonb)
- author_organization (varchar)
- article_summary (text)
- sector (varchar)

Table: people_information
- people_id (serial, primary key)
- article_id (int, not null)
- name (varchar)
- designation (varchar)
- organization (varchar)
- people_summary (text)
"""
    return schema_info


def create_prompt(nl_query: str, schema_info: str) -> str:
    return f"""
Based on the following database schema, convert this natural language query to a valid PostgreSQL SQL query.
{schema_info}

Natural language query: "{nl_query}"
Rules:
1. Only use tables from ai_analyzer schema
2. Always include the schema name (ai_analyzer) when referencing tables
3. Only return the SQL query, no explanations or comments
4. Make sure the query is valid PostgreSQL syntax
5. When searching for names, use ILIKE with wildcards (%) for case-insensitive and partial matching
6. When searching for a person by name, check both the people_information.name and spokesperson_details.name fields
7. For text searches, prefer ILIKE over = to find partial matches
8. If the query involves person names, try variations (e.g., '%John%Doe%', '%Doe%John%')
9. Include descriptive column names in the SELECT statement for clarity
10. Always use LEFT JOIN instead of INNER JOIN
11. Always include article_id in the SELECT clause
12. Order results by relevance if applicable
13. For duplicate names, prioritize spokesperson_details, then source_details, people_information, article_details, comment_details
14. Do not use DISTINCT unless required
15. Output should return article_id(s) only
"""


async def generate_sql_from_gemini(prompt: str) -> str:
    # IMPORTANT: Add your personal Google Gemini API key in the .env file before running this code
    genai.configure(api_key=settings.app.API_KEY)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    sql_query = response.text.strip()

    if sql_query.startswith("```sql"):
        sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
    elif sql_query.startswith("```"):
        sql_query = sql_query.split("```")[1].split("```")[0].strip()

    return sql_query


def get_article_details(article_ids: List[int], cursor) -> List[Dict[str, Any]]:
    placeholders = ','.join(['%s'] * len(article_ids))
    articles_query = f"""
        SELECT article_id, header, author_name, link_to_article
        FROM ai_analyzer.article_details
        WHERE article_id IN ({placeholders})
    """
    cursor.execute(articles_query, article_ids)
    article_map = {row[0]: {
        "id": row[0],
        "header": row[1],
        "author": row[2],
        "articleUrl": row[3],
        "spokespersons": [],
        "people_mentioned": []
    } for row in cursor.fetchall()}

    # Fetch Spokespersons
    cursor.execute(f"""
        SELECT article_id, name, designation, organization
        FROM ai_analyzer.spokesperson_details
        WHERE article_id IN ({placeholders})
    """, article_ids)
    for row in cursor.fetchall():
        if row[0] in article_map:
            article_map[row[0]]["spokespersons"].append({
                "name": row[1],
                "designation": row[2],
                "organization": row[3]
            })

    # Fetch People Mentioned
    cursor.execute(f"""
        SELECT article_id, name
        FROM ai_analyzer.people_information
        WHERE article_id IN ({placeholders})
    """, article_ids)
    for row in cursor.fetchall():
        if row[0] in article_map:
            article_map[row[0]]["people_mentioned"].append(row[1])

    return list(article_map.values())


async def search_articles_by_nl_query(nl_query: str) -> Dict[str, Any]:
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        schema = get_database_schema(cursor)
        sql_prompt = create_prompt(nl_query, schema)
        sql_query = await generate_sql_from_gemini(sql_prompt)

        cursor.execute(sql_query)
        results = cursor.fetchall()

        article_ids = set()
        for row in results:
            for val in row:
                if isinstance(val, int):
                    article_ids.add(val)

        if not article_ids:
            return {
                "sql_query": sql_query,
                "results": []
            }

        articles = get_article_details(list(article_ids), cursor)

        return {
            "sql_query": sql_query,
            "results": articles
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    