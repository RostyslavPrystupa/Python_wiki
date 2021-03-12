import sqlite3
import config


def select_content(name, config_database):
    if config_database != "":
        conn = sqlite3.connect(config_database)
    else:
        conn = sqlite3.connect(config.database)
    c = conn.cursor()
    c.execute("SELECT content FROM pages WHERE name=\"" + str(name) + "\"")
    answer = c.fetchone()
    conn.close()
    return answer[0]


def update_content(name, content, config_database):
    if config_database != "":
        conn = sqlite3.connect(config_database)
    else:
        conn = sqlite3.connect(config.database)    
    c = conn.cursor()
    c.execute(f"UPDATE pages SET content=\"{content}\" WHERE name=\"{name}\";")
    conn.commit()
    conn.close()
    return "ok"


def select_pages(config_database):
    if config_database != "":
        conn = sqlite3.connect(config_database)
    else:
        conn = sqlite3.connect(config.database)    
    c = conn.cursor()
    c.execute("SELECT name FROM pages ORDER BY name;")
    answer = c.fetchall()
    conn.close()
    return answer


def create_content(name, content, config_database):
    if config_database != "":
        conn = sqlite3.connect(config_database)
    else:
        conn = sqlite3.connect(config.database)
    c = conn.cursor()
    c.execute(f"INSERT INTO pages (name, content) VALUES(\"{name}\", \"{content}\");")
    conn.commit()
    conn.close()
    return "ok"
