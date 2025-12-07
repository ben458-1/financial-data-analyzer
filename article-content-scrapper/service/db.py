import json

import psycopg2
from psycopg2.extras import RealDictCursor
from core.config import data_source
from logger import log
from datetime import datetime


# setting database properties
db_params = {
    'dbname': data_source.DB_NAME,
    'host': data_source.DB_HOST,
    'user': data_source.DB_USER,
    'password': data_source.DB_PASSWORD
}


def get_db_conn():
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except Exception as conn_err:
        log.log_error('error occur while trying to establishing connection with database.', exception=conn_err)
        db_conn_close(conn)
        return None


def db_conn_close(conn):
    if conn is not None:
        conn.close()


def insert_article_data_into_db(data):
    conn = get_db_conn()

    if conn is not None:
        try:
            query = 'select articles.insert_fragmented_body( cast(%s as bigint), cast(%s as text), ' \
                    'cast(%s as text), cast(%s as text), cast(%s as text), cast(%s as integer),%s ,%s);'
            cur = conn.cursor(cursor_factory=RealDictCursor)
            article_date = None
            try:
                article_date = datetime.fromisoformat(data.get('std_date'))
            except ValueError:
                log.log_warning(f"❌ Failed to parse std_date: {data.get('std_date')}")

            cur.execute(query, (data.get('article_id'), data.get('header'), data.get('body'), data.get('author'),
                                data.get('date'), data.get('newspaper_id'),
                                article_date, datetime.now()))

            conn.commit()
        except Exception as err:
            log.log_error(f'error occur while inserting data into db. \n {err}')
        finally:
            db_conn_close(conn)


def find_article_configuration(newspaper_id):
    sql = '''
            select * from conf.articlebrowserconf a where cast(a.doc->>'newspaperID' as integer) = %s;
        '''
    conn = get_db_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (newspaper_id,))
        rs = cur.fetchone()

        article_config = {
            'article_config_id': rs.get('id'),
            'doc': rs.get('doc'),
            'userid': rs.get('userid'),
            'mgroup': rs.get('mgroup')
        }

        cur.close()  # Close the cursor to release database resources
        return article_config
    except Exception as err:
        log.log_error('error occur while fetching article configuration data in db. for more detail', exception=err)
    finally:
        db_conn_close(conn)


def fetch_auth_configuration(newspaper_id):
    sql = '''
        select * from conf.newspaper_auth_conf nac where nac.newspaper_id = %s;
    '''
    conn = get_db_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (newspaper_id,))
        rs = cur.fetchone()

        auth_config = {
            "id": rs.get("id"),
            "newspaper_id": rs.get("newspaper_id"),
            "config": rs.get("config"),
            "cookies": rs.get("cookies"),
            "cookie_last_update_at": rs.get("cookie_last_updated_at"),
            "cookie_expires_at": rs.get("cookie_expires_at"),
            "session_id_expires_at": rs.get("session_id_expires_at"),
            "use_auto_signin": rs.get("use_auto_signin")
        }

        cur.close()
        return auth_config
    except Exception as err:
        log.log_error('error occur while fetching authentication configuration data in db. for more detail',
                      exception=err)
    finally:
        db_conn_close(conn)


def fetch_newspaper_credential(newspaper_id):
    sql = '''
        select * from conf.newspaper_credential nc where nc.newspaper_id = %s and nc.valid_user;
    '''
    conn = get_db_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, (newspaper_id,))
        rs = cur.fetchone()

        auth_config = {
            "id": rs.get("id"),
            "newspaper_id": rs.get("newspaper_id"),
            "userName": rs.get("user_name"),
            "password": rs.get("password"),
            "subscription_expires_at": rs.get("subscription_expires_at"),
            "valid_user": rs.get("valid_user")
        }

        cur.close()
        return auth_config
    except Exception as err:
        log.log_error('error occur while fetching newspaper credential data in db. for more detail',
                      exception=err)
    finally:
        db_conn_close(conn)


def upsert_into_failed_articles(article_info):
    # UPSERT query
    query = """
            INSERT INTO monitoring.failed_articles (
                article_id, newspaper_id, updated_on, is_resolved, info
            )
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (article_id)
            DO UPDATE SET
                updated_on = EXCLUDED.updated_on,
                is_resolved = EXCLUDED.is_resolved,
                retry_count = monitoring.failed_articles.retry_count + 1;
    """
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        cur.execute(query, (article_info.get('article_id'),
                            article_info.get('newspaper_id'),
                            article_info.get('updated_on', datetime.now()),
                            article_info.get('is_resolved', False),
                            article_info.get('info', json.dumps({}))
                            )
                    )
        conn.commit()
        cur.close()
    except Exception as err:
        log.log_error('error occur while upsert data into failed article table in db. for more detail',
                      exception=err)
    finally:
        db_conn_close(conn)


def upsert_into_articleimages(article_info):
    # UPSERT query
    query = """
            insert into articles.articleimages(fid, url) 
            values(%s, %s) 
            on conflict(fid)
            do update set
                url = excluded.url;
    """
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        cur.execute(query, (article_info.get('article_id'), article_info.get('img_url')))
        conn.commit()
        cur.close()
    except Exception as err:
        log.log_error('error occur while upsert data into article images table in db. for more detail',
                      exception=err)
    finally:
        db_conn_close(conn)


def get_failed_articles_by_article_id(article_id):
    conn = get_db_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM monitoring.failed_articles WHERE article_id = %s;",
            (article_id,)
        )
        rs = cur.fetchone()

        if rs is None:
            return None

        failed_article = {
            "article_id": rs.get("article_id"),
            "newspaper_id": rs.get("newspaper_id"),
            "failure_at": rs.get("failure_at"),
            "updated_on": rs.get("updated_on"),
            "is_resolved": rs.get("is_resolved"),
            "info": rs.get("info") if rs.get("info") else None
        }

        cur.close()
        return failed_article
    except Exception as err:
        log.log_error('error occur while fetching failed article by article_id data in db. for more detail',
                      exception=err)
    finally:
        db_conn_close(conn)


def get_failed_articles_by_newspaper_id(newspaper_id):
    conn = get_db_conn()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM monitoring.failed_articles WHERE newspaper_id = %s;",
            (newspaper_id,)
        )
        rs = cur.fetchall()

        failed_articles = []

        if rs is None:
            return None

        for row in rs:
            article = {
                "article_id": row.get("article_id"),
                "newspaper_id": row.get("newspaper_id"),
                "failure_at": row.get("failure_at"),
                "updated_on": row.get("updated_on"),
                "is_resolved": row.get("is_resolved"),
                "info": row.get("info") if row.get("info") else None
            }
            failed_articles.append(article)

        cur.close()
        return failed_articles
    except Exception as err:
        log.log_error('error occur while fetching failed article by article_id data in db. for more detail',
                      exception=err)
    finally:
        db_conn_close(conn)
