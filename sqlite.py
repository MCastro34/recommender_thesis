from random import randint, random
import sqlite3
from sqlite3 import Error


def connect(db):
    return sqlite3.connect(db)


def create_table(conn):
    try:
        conn.execute(
            'CREATE TABLE USERS (USER TEXT NOT NULL,ITEM TEXT NOT NULL,RATE INT NOT NULL, PRIMARY KEY (USER, ITEM));')
    except Error as e:
        print(e)


def list_all(conn):
    cursor = conn.execute("SELECT user, item, rate FROM USERS;")
    # if len(list(cursor)) <= 0:
    #     print("list is empty")
    result = []
    for row in cursor:
        u = {"user": row[0], "item": row[1], "rate": row[2]}
        result.append(u)
    return result


def exist_user(conn, user):
    query = "SELECT user FROM USERS WHERE user='" + user + "' GROUP BY user;"
    cursor = conn.execute(query)
    # if len(list(cursor)) <= 0:
    #     print("list is empty")
    result = []
    for row in cursor:
        u = {"user": row[0]}
        result.append(u)
    return result


def list_users(conn):
    cursor = conn.execute("SELECT user FROM USERS GROUP BY user;")
    # if len(list(cursor)) <= 0:
    #     print("list is empty")
    result = []
    for row in cursor:
        u = {"user": row[0]}
        result.append(u)
    return result


def insert_user(conn, user, item, rate):
    try:
        conn.execute(
            'INSERT INTO USERS (USER,ITEM,RATE) VALUES (?,?,?)', (user, item, rate))
        conn.commit()
    except Error as e:
        print(e)


def close(conn):
    conn.close()


def populate_db(db):
    conn = connect(db)
    create_table(conn)
    for i in range(0, 10):
        user = f"user_{i}"
        print(user)
        for j in range(0, 10):
            rate_prob = random()
            if rate_prob > 0.3:
                item = f"item_{j}"
                rate = randint(1, 5)
                print(item, " - ", rate)
                insert_user(conn, user, item, rate)
    close(conn)


def create(db):
    conn = connect(db)
    create_table(conn)


def list(db):
    conn = connect(db)
    print(list_all(conn))
    close(conn)
