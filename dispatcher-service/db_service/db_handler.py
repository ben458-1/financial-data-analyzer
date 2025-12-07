import psycopg2
from psycopg2.extras import RealDictCursor
from conf.config_manager import config_manager

db_params = config_manager.get_db_param()


def get_article_conf():
    conn = None
    sql = '''
        select 
             a.doc, a.newspaper_id, a.priority,
             n.currency, n.isactive, n.link, 
             n.name, l."name" as lang, r.name as region 
        from conf.articlesearchconf a
        left join conf.newspapers n on n.id = a.newspaper_id
        left join conf.languages l on l.id = n.language_id
        left join conf.regions r on r.id = n.region_id
        ;
    '''

    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        result_sets = cur.fetchall()
        article_configurations = []
        for rs in result_sets:
            article_config = {
                'doc': rs.get('doc'),
                'newspaper_id': rs.get('newspaper_id'),
                'priority': rs.get('priority'),
                'currency': rs.get('currency'),
                'is_active': rs.get('isactive'),
                'website_url': rs.get('link'),
                'source_name': rs.get('name'),
                'language': rs.get('lang'),
                'region': rs.get('region')
            }
            article_configurations.append(article_config)

        cur.close()     # Close the cursor to release database resources
        return article_configurations
    except Exception as err:
        print('check error', err)
        return []
    finally:
        if conn is not None:
            conn.close()    # close the database connection
