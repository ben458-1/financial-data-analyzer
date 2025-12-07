import psycopg2
from psycopg2.extras import Json
from psycopg2 import DatabaseError
from app.logger import log
from app.core.config import settings
from psycopg2.extras import Json


# Establish DB connection
try:
    conn = psycopg2.connect(
        dbname=settings.db.NAME,
        user=settings.db.USER,
        password=settings.db.PASSWORD,
        host=settings.db.HOST,
        port=settings.db.PORT
    )
    cursor = conn.cursor()
    log.log_info("Database connection established.")
except Exception as e:
    log.log_error(f"Error establishing database connection: {e}")
    conn = None
    cursor = None


def join_list_as_word(input_list, delimiter="/#/"):
    """
    Join elements of a list into a single word using the given delimiter.
    Accepts single strings or lists.
    """
    if input_list is None:
        return ""
    if isinstance(input_list, str):
        return input_list
    if not isinstance(input_list, list):
        raise ValueError("Input must be a list or string")
    return delimiter.join(str(item) for item in input_list)



def insert_to_article_details(individual_article_json_data, article_id, newspaper_id, header, link_to_article, sector, article_keywords,article_summary):
    
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return None

    try:
        sql = """
        INSERT INTO ai_analyzer.article_details (
            article_id,
            newspaper_id,
            header,
            link_to_article,
            sector,
            author_name, 
            author_comments,
            author_designation, 
            author_organization, 
            article_keywords,
            article_summary
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING article_id;
        """

        author_name = individual_article_json_data.get("name")
        author_comments = join_list_as_word(individual_article_json_data.get("comments"))

        # Fix: Handle designation properly whether it's a dict or string
        designation_data = individual_article_json_data.get("designation", {})
        if not isinstance(designation_data, dict):
            designation_data = {"current_designation": str(designation_data)}
        author_designation = Json(designation_data)

        author_organization = individual_article_json_data.get("organization", "NA")
       # article_keywords = join_list_as_word(individual_article_json_data.get("article_keywords"))
        # print("🧪 article_keywords =", article_keywords, "| type:", type(article_keywords))
        # print("🧪 article_summary =", article_summary)
        # article_summary = individual_article_json_data.get("article_summary", "NA")

        values = (
            article_id,
            newspaper_id,
            header,
            link_to_article,
            sector,
            author_name,
            author_comments,
            author_designation,
            author_organization,
            article_keywords,
            article_summary
        )

        cursor.execute(sql, values)
        inserted_id = cursor.fetchone()[0]
        conn.commit()
        log.log_info(f"Article inserted successfully with ID: {inserted_id}")
        return inserted_id

    except Exception as e:
        log.log_error(f"Error during article insertion: {e}")
        conn.rollback()
        return None




def insert_people_info_from_article(individual_people_info_json, article_id):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return None

    try:
        

        sql = """
        INSERT INTO ai_analyzer.people_information (
            article_id,
            name,
            designation,
            organization,
            people_summary
        )
        VALUES (%s, %s, %s, %s, %s)
        """

       
        name = individual_people_info_json.get("name")
        designation = individual_people_info_json.get("designation", "NA")
        organization = individual_people_info_json.get("company", "NA")
        people_summary = individual_people_info_json.get("people_summary", "NA")
        values = (
            article_id,
            name,
            designation,
            organization,
            people_summary
        )

        cursor.execute(sql, values)

        conn.commit()
        log.log_info("People info inserted successfully.")
        return article_id
    except Exception as e:
        log.log_error(f"Error inserting into people_information: {e}")
        conn.rollback()
        return None


def insert_to_spokesperson_details(individual_spokesperson_json_data, article_id):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return None

    try:
        sql = """
        INSERT INTO ai_analyzer.spokesperson_details (
            article_id,
            name,
            designation,
            organization,
            spk_place_location,
            spk_place_state,
            spk_place_country,
            people_in_comments,
            competitors_mentioned,
            spk_past_designation,
            spk_past_organization,
            spk_past_no_of_years,
            spk_past_time_period,
            spk_past_location,
            spk_past_country,
            spk_summary,
            comment_date
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s
        )
        RETURNING spokesperson_id;
        """

        spk_place_json = individual_spokesperson_json_data.get('spokesperson_place', {})
        spk_past_json = individual_spokesperson_json_data.get('spokesperson_past', {})
        people_in_comments = join_list_as_word(individual_spokesperson_json_data.get("people_in_comment"))
        competitors_mentioned = join_list_as_word(individual_spokesperson_json_data.get("competitors_mentioned"))
        
        comment_date = Json(individual_spokesperson_json_data.get("comment_date", {"date": "NA", "abstract": "NA"}))


        values = (
            article_id,
            individual_spokesperson_json_data.get("attribution") or individual_spokesperson_json_data.get("attribution_name"),
            individual_spokesperson_json_data.get("designation"),
            individual_spokesperson_json_data.get("organization"),
            spk_place_json.get("location"),
            spk_place_json.get("state"),
            spk_place_json.get("country"),
            people_in_comments,
            competitors_mentioned,
            spk_past_json.get("designation"),
            spk_past_json.get("organization"),
            spk_past_json.get("no_of_years"),
            spk_past_json.get("timeperiod"),
            spk_past_json.get("location"),
            spk_past_json.get("country"),
           individual_spokesperson_json_data.get("spokesperson_summary"),
            comment_date
        )

        cursor.execute(sql, values)
        spokesperson_id = cursor.fetchone()[0]
        conn.commit()
        log.log_info(f"Spokesperson inserted with ID: {spokesperson_id}")
        return spokesperson_id

    except Exception as e:
        log.log_error(f"Error inserting into spokeperson_details: {e}")
        conn.rollback()
        return None


def insert_to_source_details(individual_source_json_data, article_id):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return None

    try:
        sql = """
        INSERT INTO ai_analyzer.source_details (
            article_id,
            designation,
            organization,
            people_in_comments,
            competitors_mentioned,
            comment_date
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING source_id;
        """

        people_in_comments = join_list_as_word(individual_source_json_data.get("people_in_comment"))
        competitors_mentioned = join_list_as_word(individual_source_json_data.get("competitors_mentioned"))
       
        comment_date = Json(individual_source_json_data.get("comment_date", {"date": "NA", "abstract": "NA"}))


        values = (
            article_id,
            individual_source_json_data.get("designation"),
            individual_source_json_data.get("organization"),
            people_in_comments,
            competitors_mentioned,
            comment_date
        )

        cursor.execute(sql, values)
        source_id = cursor.fetchone()[0]
        conn.commit()
        log.log_info(f"Source inserted with ID: {source_id}")
        return source_id

    except Exception as e:
        log.log_error(f"Error inserting into source_details: {e}")
        conn.rollback()
        return None


def insert_comment_details(comment_json, spokesperson_id, source_id):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return

    try:
        sql = """
        INSERT INTO ai_analyzer.comment_details (
            spokesperson_id,
            source_id,
            comment,
            reference_type,
            from_to,
            comment_keywords,
            stk_in_the_com
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            spokesperson_id,
            source_id,
            comment_json.get("comment"),
            comment_json.get("reference_type"),
            join_list_as_word(comment_json.get("from_to")),
            join_list_as_word(comment_json.get("comment_keywords")),
            join_list_as_word(comment_json.get("stakeholders_in_comment"))
        )

        cursor.execute(sql, values)
        conn.commit()
        log.log_info("Comment inserted.")

    except Exception as e:
        log.log_error(f"error inserting comment: {e}")
        conn.rollback()


def insert_into_entire_table(json_data, article_id, newspaper_id, header, link_to_article, sector):
    if conn is None or cursor is None:
        log.log_error("Database connection is not available.")
        return

    extraction_details = json_data.get("extraction_details", [])
    article_details = json_data.get("article_details", {})
    author_details = json_data.get("author_details", {})
    article_keywords = join_list_as_word(article_details.get("article_keywords"))
    article_summary = article_details.get("article_summary", "NA")
    people_info_details = article_details.get("people_info", [])
    inserted_article_id = insert_to_article_details(author_details, article_id, newspaper_id, header, link_to_article, sector,article_keywords, article_summary)

    if inserted_article_id is None:
        log.log_error("Failed to insert article.")
        return
    for individual_people_info_json in people_info_details:
        insert_people_info_from_article(individual_people_info_json,inserted_article_id)


    
    
    

    # Step 3: Insert each attribution + comments
    for entry in extraction_details:
        spokesperson_id = None
        source_id = None

        if entry.get("attribution_type") == "spokesperson":
            spokesperson_id = insert_to_spokesperson_details(entry, inserted_article_id)
        else:
            source_id = insert_to_source_details(entry, inserted_article_id)

        
        for comment in entry.get("comment_details", []):
            if not spokesperson_id and not source_id:
                 log.log_info("Skipping comment insertion due to missing foreign keys.")
                 continue
            insert_comment_details(comment, spokesperson_id, source_id)


def upsert_validation_failed_article(article_id: int, newspaper_id: int):
    """
    Insert into validation_failed_article or update retry_attempt and last_updated_on if conflict.
    
    Args:
        conn: psycopg2 connection object
        article_id: int - ID of the article
        newspaper_id: int - ID of the newspaper
        log: optional logger with .log_error method
    """
    try:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO ai_analyzer.validation_failed_article (article_id, newspaper_id)
            VALUES (%s, %s)
            ON CONFLICT (article_id, newspaper_id)
            DO UPDATE SET 
                retry_attempt = ai_analyzer.validation_failed_article.retry_attempt + 1,
                last_updated_on = now();
            """
            cursor.execute(query, (article_id, newspaper_id))
            log.log_info(f"Parsing failed article inserted into db, article_id {article_id}")
        conn.commit()
    except (DatabaseError, Exception) as e:
        conn.rollback()
        log.log_error(f"Failed to upsert validation_failed_article: {e}")
