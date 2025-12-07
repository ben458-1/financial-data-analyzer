import psycopg2
import os
from dotenv import load_dotenv
from psycopg2.extras import Json
import json

load_dotenv()

try:
    conn = psycopg2.connect(
        dbname=os.getenv("DBNAME"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )
    cursor = conn.cursor()
    print("Database connection established.")
except Exception as e:
    print(f"Error establishing database connection: {e}")
    conn = None
    cursor = None

if conn and cursor:
    try:
        ddl = """
CREATE SCHEMA IF NOT EXISTS ai_new AUTHORIZATION postgres;


CREATE SEQUENCE IF NOT EXISTS ai_new.spokesperson_id_seq
    INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE;


CREATE SEQUENCE IF NOT EXISTS ai_new.source_id_seq
    INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE;


CREATE SEQUENCE IF NOT EXISTS ai_new.comment_id_seq
    INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE;


CREATE SEQUENCE IF NOT EXISTS ai_new.article_id_seq
    INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE;

CREATE SEQUENCE IF NOT EXISTS ai_new.people_id_seq
    INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE;



CREATE TABLE IF NOT EXISTS ai_new.spokesperson_details (
    spokesperson_id serial PRIMARY KEY,
    article_id int NOT NULL,
    name varchar NULL,
    designation varchar NULL,
    organization varchar NULL,
    spk_place_location varchar NULL,
    spk_place_state varchar NULL,
    spk_place_country varchar NULL,
    people_in_comments text NULL,
    competitors_mentioned text NULL,
    spk_past_designation varchar NULL,
    spk_past_organization varchar NULL,
    spk_past_no_of_years int NULL,
    spk_past_time_period varchar NULL,
    spk_past_location varchar NULL,
    spk_past_country varchar NULL,
    spk_summary text NULL,
    comment_date jsonb NULL
);


CREATE TABLE IF NOT EXISTS ai_new.source_details (
    source_id serial PRIMARY KEY,
    article_id int NOT NULL,
    designation varchar NULL,
    organization varchar NULL,
    people_in_comments text NULL,
    competitors_mentioned text NULL,
    comment_date jsonb NULL
);


CREATE TABLE IF NOT EXISTS ai_new.comment_details (
    comment_id serial PRIMARY KEY,
    spokesperson_id int NULL,
    source_id int NULL,
    comment varchar NULL,
    reference_type varchar NULL,
    from_to text NULL,
    comment_keywords text NULL,
    stk_in_the_com text NULL,
    CONSTRAINT fk_spokesperson
        FOREIGN KEY (spokesperson_id)
        REFERENCES ai_new.spokesperson_details(spokesperson_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_source
        FOREIGN KEY (source_id)
        REFERENCES ai_new.source_details(source_id)
        ON DELETE CASCADE,
    CONSTRAINT ensure_one_fk CHECK (
        spokesperson_id IS NOT NULL OR source_id IS NOT NULL
    )
);



CREATE TABLE IF NOT EXISTS ai_new.article_details (
    id serial PRIMARY KEY,
    article_id int NOT NULL,
    newspaper_id int NOT NULL,
    header varchar NULL,
    link_to_article varchar NULL,
    article_keywords text NULL,
    author_name varchar NULL,
    author_comments text NULL,
    author_designation jsonb NULL,
    author_organization varchar NULL,
    article_summary text NULL,
    sector varchar NULL
);


CREATE TABLE IF NOT EXISTS ai_new.people_information (
    people_id serial PRIMARY KEY,
    article_id int NOT NULL,
    name varchar NULL,
    designation varchar NULL,
    organization varchar NULL,
    people_summary text NULL
);

"""

        cursor.execute(ddl)
        conn.commit()
        print("Schema and tables created successfully.")
    except Exception as e:
        print(f"Error executing DDL: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
else:
    print("Connection or cursor is not available. Skipping schema setup.")