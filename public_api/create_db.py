import psycopg2
def meme_db_create():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="admin", host="db")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = '''DROP DATABASE IF EXISTS meme;'''
    cursor.execute(sql)
    sql = '''CREATE DATABASE meme
            WITH 
            OWNER = postgres
            ENCODING = 'UTF8'
            TABLESPACE = pg_default
            CONNECTION LIMIT = -1;'''
    try:
        cursor.execute(sql)
    except psycopg2.Error as e:
        print("Error creating database:", e)
    conn.commit()
    cursor.close()
    conn.close()
    conn = psycopg2.connect(dbname="meme", user="postgres", password="admin",
                            host="db")
    cursor = conn.cursor()
    conn.autocommit = True
    sql1 = '''
    DROP TABLE IF EXISTS meme CASCADE;
    CREATE TABLE meme(
          id                 BIGSERIAL,
          name               VARCHAR   NOT NULL,
          link               VARCHAR   NOT NULL,
          UNIQUE(name),
          PRIMARY KEY(id)
        );
    '''
    cursor.execute(sql1)
    conn.commit()
    print("Database created successfully........")

    # Closing the connection

    cursor.close()
    conn.close()


meme_db_create()


