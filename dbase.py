import sqlite3 as sql
from config import ADMIN_ID, DEVELOPER_ID

con = sql.connect('db.db')
cur = con.cursor()


# создание таблиц
with open('create.sql') as f:
    cur.executescript(f.read())
con.commit()


async def add_media(tgid, image_filename, media_type):
    cur.execute(f"INSERT INTO media VALUES ('{tgid}', '{image_filename}', '{media_type}')")
    con.commit()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


async def search_media(search_string, method, offset=0):
    con.row_factory = dict_factory  # sql.Row
    c = con.cursor()
    if method == "search":
        req = "SELECT * FROM media WHERE "
        for word in search_string.split():
            try:
                string_int = int(word)
                req += f" (tgid = '{string_int}') OR "
            except ValueError:
                return []
        req = req[0:-4] + " ORDER BY rowid DESC"
    elif method == "last5":
        req = f'''
                SELECT * FROM media
                    ORDER BY rowid DESC
                    LIMIT 5 OFFSET {offset}
                '''
    else:  # all
        req = f'''
                SELECT * FROM media
                    ORDER BY rowid DESC
                '''
    print(req)
    try:
        c.execute(req)
    except Exception:
        return []
    else:
        return c.fetchall()


async def user_is_admin(tgid):
    cur.execute(f"SELECT * FROM managers WHERE tgid = " + str(tgid))
    rows = cur.fetchall()
    return (ADMIN_ID == tgid) or (DEVELOPER_ID == tgid) or (len(rows) > 0)


async def add_manager(tgid):
    cur.execute(f"INSERT INTO managers VALUES ('{tgid}')")
    con.commit()


async def delete_manager(tgid):
    cur.execute(f"DELETE FROM managers WHERE tgid = '{tgid}'")
    con.commit()


async def all_managers():
    cur.execute(f"SELECT * FROM managers")
    return cur.fetchall()


async def add_user(tgid, chat_id):
    cur.execute(f"SELECT * FROM users WHERE tgid = " + str(tgid))
    rows = cur.fetchall()
    if len(rows) == 0:
        cur.execute(f"INSERT INTO users VALUES ('{tgid}','{chat_id}', '1')")
        con.commit()


async def all_users():
    cur.execute(f"SELECT * FROM users")
    return cur.fetchall()


async def delete_all_users():
    cur.execute(f"DELETE FROM users")
    return cur.fetchall()


async def all_broadcast_messages():
    cur.execute(f"SELECT * FROM broadcastmessages")
    return cur.fetchall()
