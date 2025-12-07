import psycopg2
import os
import json
from typing import List
from app.logger import log
from app.core.config import settings
 
try:
    conn = psycopg2.connect(
        dbname=settings.db.NAME,
        user=settings.db.USER,
        password=settings.db.PASSWORD,
        host=settings.db.HOST,
        port=settings.db.PORT
    )
    cursor = conn.cursor() # Create a cursor at module level
    log.log_info("Database connection established.")
except Exception as e:
    log.log_error(f"Error establishing database connection: {e}")
    conn = None # sets conn to none, so that it can be checked.
    cursor = None

def split_delimited_string(value: str, delimiter="/#/"):
    if not value or not isinstance(value, str):
        return []
    return [item.strip() for item in value.split(delimiter) if item.strip()]

def fetch_article_details(article_id):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return
    try:
        query = """
            SELECT header, link_to_article, article_keywords, author_name, author_comments, author_designation, author_organization, article_summary, sector
            FROM ai_analyzer.article_details
            WHERE article_id = %s ;
        """
        cursor.execute(query, (article_id,))
        results = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        
    except psycopg2.Error as e:
        log.log_error(f"Database query error (summary): {e}")
        results = []
        colnames = []
    except Exception as e:
        log.log_error(f"An unexpected error during summary fetch: {e}")
        results = []
        colnames = []
    
    return results, colnames
 
# --- THIS IS THE FUNCTION NEEDED FOR THE ATTRIBUTION LIST PAGE ---
def fetch_people_information(article_id: int):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return
 
    try:
        query = """
            SELECT name, designation, organization, people_summary
            FROM ai_analyzer.people_information
            WHERE article_id = %s;
        """
        cursor.execute(query, (article_id,))
        results = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
    except psycopg2.Error as e:
        log.log_error(f"Database query error (attributions): {e}")
        results = []
        colnames = []
    except Exception as e:
        log.log_error(f"An unexpected error occurred during attribution fetch: {e}")
        results = []
        colnames = []
    
    return results, colnames
 
# --- fetch_full_article_data definition - keep this for the final detail page ---
def fetch_source_details(article_id: int):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return
    try:
        query = """
            SELECT source_id, designation, organization, people_in_comments, competitors_mentioned, comment_date
            FROM ai_analyzer.source_details
            WHERE article_id = %s"""
        cursor.execute(query, (article_id,))
        rows = cursor.fetchall()
        source_ids = [row[0] for row in rows]
        results = [row[1:] for row in rows]
        colnames = [desc[0] for desc in cursor.description]
    except psycopg2.Error as e:
        log.log_error(f"Database query error (full fetch): {e}")
        results  = []
    except Exception as e:
        log.log_error(f"An unexpected error during full fetch: {e}")
        colnames = []
    
    return source_ids, results, colnames
 
def fetch_spokesperson_details(article_id: int):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return
    try:
        query = """
            SELECT spokesperson_id, name, designation, organization, spk_place_location, spk_place_state, spk_place_country, people_in_comments, competitors_mentioned, spk_past_designation, spk_past_organization, spk_past_no_of_years, spk_past_time_period, spk_past_location, spk_past_country, spk_summary, comment_date
            FROM ai_analyzer.spokesperson_details
            WHERE article_id = %s"""
        cursor.execute(query, (article_id,))
        rows = cursor.fetchall()
        spk_ids = [row[0] for row in rows]
        results = [row[1:] for row in rows]
        colnames = [desc[0] for desc in cursor.description]
    except psycopg2.Error as e:
        log.log_error(f"Database query error (full fetch): {e}")
        results  = []
    except Exception as e:
        log.log_error(f"An unexpected error during full fetch: {e}")
        colnames = []
    
    return spk_ids, results, colnames
 
 
def fetch_comment_details_by_spokesperson(spokesperson_id: int):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return
    try:
        query = """
            SELECT comment, reference_type, from_to, comment_keywords, stk_in_the_com
            FROM ai_analyzer.comment_details
            WHERE spokesperson_id = %s"""
        cursor.execute(query, (spokesperson_id, ))
        results = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
    except psycopg2.Error as e:
        log.log_error(f"Database query error (full fetch): {e}")
        results  = []
    except Exception as e:
        log.log_error(f"An unexpected error during full fetch: {e}")
        colnames = []
    
    return results, colnames
 
def fetch_comment_details_by_source(source_id: int):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return [], []
 
    try:
        query = """
            SELECT comment, reference_type, from_to, comment_keywords, stk_in_the_com
            FROM ai_analyzer.comment_details
            WHERE source_id = %s
        """
        cursor.execute(query, (source_id,))
        results = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
    except psycopg2.Error as e:
        log.log_error(f"Database query error (comment_details by source): {e}")
        results = []
        colnames = []
    except Exception as e:
        log.log_error(f"Unexpected error fetching comments by source: {e}")
        results = []
        colnames = []
 
    return results, colnames
 
def fetch_full_article_json(article_id: int):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return {}
 
    # article_data = {}
    article_details = {}
    
    # Article details
    # article_results, article_cols = fetch_article_details(article_id)
    # article_details["article_keywords"] = ["Datawork", "analytics"] #Have to change it later with delimiter reversal
    # article_details["article_summary"] = article_results[0][7]
    article_results, article_cols = fetch_article_details(article_id)

        # Defensive check in case no data is returned
    if not article_results:
        article_details = {
            "article_keywords": [],
            "article_summary": ""
        }
    else:
        row = dict(zip(article_cols, article_results[0]))

        keyword_list = split_delimited_string(row.get("article_keywords", ""))
        article_details = {
            "article_keywords": keyword_list,
            "article_summary": row.get("article_summary", "")
        }

    
    # author_details = {}
    # author_details["name"] = article_results[0][3]
    # author_details["comments"] = [article_results[0][4]]
    # author_details["designation"] = {
    #     "current_designation": "For Now",
    #     "past_designation": "For Now"
    # }
    # author_details["organization"] = article_results[0][6]
    author_details = {}

    author_details["name"] = article_results[0][3]
    author_details["comments"] = split_delimited_string(article_results[0][4])  # handles /#/ separated comments

    # Parse designation safely if stored as JSONB or dict string
    try:
        designation_data = json.loads(article_results[0][5]) if article_results[0][5] else {}
    except Exception:
        designation_data = {}

    author_details["designation"] = {
        "current_designation": designation_data.get("current_designation", "NA"),
        "past_designation": designation_data.get("past_designation", "NA")
    }

    author_details["organization"] = article_results[0][6]

    # if not article_results:
    #     author_details = {
    #     "name": "",
    #     "comments": [],
    #     "designation": {
    #         "current_designation": "",
    #         "past_designation": ""
    #     },
    #     "organization": ""
    # }
    # else:
    #     row = dict(zip(article_cols, article_results[0]))

    # # Assume comments are stored as a string joined by "||"
    # author_comments = row["author_comments"] or ""
    # comment_list = [comment.strip() for comment in author_comments.split("||") if comment.strip()]

    # author_details = {
    #     "name": row["author_name"],
    #     "comments": comment_list,
    #     "designation": {
    #         "current_designation": row["author_designation"],
    #         "past_designation": "Unknown"  # Replace if stored elsewhere
    #     },
    #     "organization": row["author_organization"]
    # }


    # People info
    # people_info = {}
  
    # people_results, people_cols = fetch_people_information(article_id)
    # people_info = list(dict(zip(people_cols, row)) for row in people_results)
    # people_results, people_cols = fetch_people_information(article_id)

    # people_info = []
    # for row in people_results:
    #     person = dict(zip(people_cols, row))
    #     people_info.append({
    #     "name": person["name"],
    #     "summary": person["people_summary"],
    #     "designation": person["designation"],
    #     "company": person["organization"]
    # })
    people_results, people_cols = fetch_people_information(article_id)
    people_info = []

    for row in people_results:
        person = dict(zip(people_cols, row))
        formatted = {
            "name": person["name"],
            "summary": person.get("people_summary", "NA"),
            "designation": person["designation"],
            "company": person["organization"]
        }
        people_info.append(formatted)


   
   
    
 
    # # Source details
    # Source details
    source_ids, source_results, source_cols = fetch_source_details(article_id)
    source_entries = []

    for source_id, row in zip(source_ids, source_results):
        raw_entry = dict(zip(source_cols[1:], row))  # exclude source_id
        comment_date_value = raw_entry.get("comment_date", {})
        structured_entry = {
            "designation": raw_entry.get("designation", ""),
            "organization": raw_entry.get("organization", ""),
            "people_in_comment": split_delimited_string(raw_entry.get("people_in_comments", [])) or [],
            "competitors_mentioned": split_delimited_string(raw_entry.get("competitors_mentioned", [])) or [],
            
            "comment_date" :{
                "date": comment_date_value.get("date", "NA"),
                "abstract": comment_date_value.get("abstract", "NA")
                },


            # "comment_date": {
            #     "date": raw_entry.get("comment_date", "Unknown"),
            #     "abstract": "For now"  # Replace with actual summary/abstract if available
            # },
            "comment_details": []
        }

        # Fetch comments for this source
        comments, comment_cols = fetch_comment_details_by_source(source_id)
        for com in comments:
            com_dict = dict(zip(comment_cols, com))
            structured_entry["comment_details"].append({
                "comment": com_dict["comment"],
                "reasoning": com_dict.get("reasoning", "For now"),
                "reference_type": com_dict.get("reference_type", "indirect"),
                #"from_to": com_dict.get("from_to", ["source", "public"]),
                "from_to": split_delimited_string(com_dict.get("from_to", "")),
                #"comment_keywords": com_dict.get("comment_keywords", ["keyword1"]),
                "comment_keywords": split_delimited_string(com_dict.get("comment_keywords", "")),

                #"stakeholders_in_comment": com_dict.get("stk_in_the_com", ["stakeholder"])
                "stakeholders_in_comment": split_delimited_string(com_dict.get("stk_in_the_com", ""))
            })

        source_entries.append(structured_entry)

    # source_ids, source_results, source_cols = fetch_source_details(article_id)
    # source_entries = []
    # for source_id, row in zip(source_ids, source_results):
    #     entry = dict(zip(source_cols[1:], row))  # exclude source_id
    #     entry["source_id"] = source_id
 
    #     if source_id is not None:
    #         comments, comment_cols = fetch_comment_details_by_source(source_id)
    #         entry["comments"] = [
    #             dict(zip(comment_cols, com)) for com in comments
    #         ] if comments else []
 
    #     source_entries.append(entry)
    #     for source in source_entries:
    #         source.pop("competitors_mentioned")
    #         source["designation"] = "designation"
    #         source["organization"] = "organization"
    #         source["people_in_comments"] = ["Only brackets problem for now"]


         
    #         for ind_comments in source["comments"]:
    #             ind_comments["reasoning"]= "For now"
    #             ind_comments["from_to"]= ["for now from", "for now to"]
    #             ind_comments["comment_keywords"] = ["for now keywords"]
    #             ind_comments["stk_in_the_com"] = ["for now"]
    #         source["comment_date"] = {
    #         "date": "For now",
    #         "abstract": "For now"
    #     } 
       
        
        
 
 
    # # Spokesperson details
    # spk_ids, spk_results, spk_cols = fetch_spokesperson_details(article_id)
    # spokesperson_entries = []
    # for spk_id, row in zip(spk_ids, spk_results):
    #     entry = dict(zip(spk_cols[1:], row))  # exclude spokesperson_id
    #     entry["spokesperson_id"] = spk_id
 
    #     if spk_id is not None:
    #         comments, comment_cols = fetch_comment_details_by_spokesperson(spk_id)
    #         entry["comments"] = [
    #             dict(zip(comment_cols, com)) for com in comments
    #         ] if comments else []
 
    #     spokesperson_entries.append(entry)
    
    # for person in spokesperson_entries:
    #     person.pop("competitors_mentioned")
    #     person["name_type"] = "spokesperson"
    #     person["spokesperson_place"] = {
    #         "location": person.pop("spk_place_location"),
    #         "state": person.pop("spk_place_state"),
    #         "country": person.pop("spk_place_country"),
    #     }
    #     person["spokesperson_past"] = {
    #         "designation": person.pop("spk_past_designation"),
    #         "organization": person.pop("spk_past_organization"),
    #         "no_of_years": person.pop("spk_past_no_of_years"),
    #         "timeperiod": person.pop("spk_past_time_period"),
    #         "location": person.pop("spk_past_location"),
    #         "country": person.pop("spk_past_country")
    #     }
    #     for ind_comments in person["comments"]:
    #         ind_comments["reasoning"]= "For now"
    #         ind_comments["from_to"]= ["for now from", "for now to"]
    #         ind_comments["comment_keywords"] = ["for now keywords"]
    #         ind_comments["stk_in_the_com"] = ["for now"]
    #     person["comment_date"] = {
    #         "date": "For now",
    #         "abstract": "For now"
    #     }    
    #     person["people_in_comments"] = ["Only brackets problem for now"]
    # return spokesperson_entries, source_entries, article_details, people_info, author_details
    # Spokesperson details
    # Spokesperson details
    spk_ids, spk_results, spk_cols = fetch_spokesperson_details(article_id)
    spokesperson_entries = []

    for spk_id, row in zip(spk_ids, spk_results):
        entry = dict(zip(spk_cols[1:], row))  # exclude spokesperson_id
        entry["spokesperson_id"] = spk_id

        if spk_id is not None:
            comments, comment_cols = fetch_comment_details_by_spokesperson(spk_id)
            entry["comments"] = [
                dict(zip(comment_cols, com)) for com in comments
            ] if comments else []

        spokesperson_entries.append(entry)

    for person in spokesperson_entries:
        # ✅ Remove unused
        person.pop("competitors_mentioned", None)

        # ✅ Rename to match frontend
        person["attribution"] = person.pop("name")
        person["attribution_type"] = "spokesperson"
        person["comment_details"] = person.pop("comments")
        person["spokesperson_summary"] = person.pop("spk_summary")

        # ✅ Nested structures
        person["spokesperson_place"] = {
            "location": person.pop("spk_place_location"),
            "state": person.pop("spk_place_state"),
            "country": person.pop("spk_place_country"),
        }
        person["spokesperson_past"] = {
            "designation": person.pop("spk_past_designation"),
            "organization": person.pop("spk_past_organization"),
            "no_of_years": person.pop("spk_past_no_of_years"),
            "timeperiod": person.pop("spk_past_time_period"),
            "location": person.pop("spk_past_location"),
            "country": person.pop("spk_past_country")
        }

        # ✅ Fill each comment with defaults if missing
        for ind_comments in person["comment_details"]:
            ind_comments["reasoning"] = ind_comments.get("reasoning", "NA")
            ind_comments["from_to"] = split_delimited_string(ind_comments.get("from_to", ["Unknown", "Unknown"]))
            ind_comments["comment_keywords"] = split_delimited_string(ind_comments.get("comment_keywords", ["NA"]))
            ind_comments["stakeholders_in_comment"] = split_delimited_string(ind_comments.get("stk_in_the_com", ["NA"]))
            if "stk_in_the_com" in ind_comments:
                del ind_comments["stk_in_the_com"]

        # ✅ Consistent key for comment date
        person["comment_date"] = {
            "date": person.get("comment_date", {}).get("date", "NA"),
            "abstract": person.get("comment_date", {}).get("abstract", "NA")
        }

        # ✅ Set empty if needed
        person["people_in_comment"] = split_delimited_string(person.get("people_in_comments", []))
        if "people_in_comments" in person:
            del person["people_in_comments"]

    return spokesperson_entries, source_entries, article_details, people_info, author_details
 
# result, names = fetch_article_details(4)
# print("article_results", result)
# print("article_names", names)

# spokesperson_info, source_info, article_info, people_info, author_info  = fetch_full_article_json(100)
#print(json.dumps(spokesperson_info, indent=2))
#print(json.dumps(source_info, indent=2))
#print(json.dumps(article_info, indent=2))
# print(json.dumps(people_info, indent=2))
#print(json.dumps(author_info, indent=2))