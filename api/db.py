import sqlite3

con = sqlite3.connect("qc.db")

QUESTIONS = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT)"
CHOICES = "CREATE TABLE IF NOT EXISTS choices (id INTEGER PRIMARY KEY, question_id INTEGER,answer TEXT)"

# KEEP IN CRUD ORDER


def create_schema():
    cur = con.cursor()
    cur.execute(QUESTIONS)
    cur.execute(CHOICES)
    con.commit()


def insert_question(question, answer) -> bool:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO questions (question, answer) VALUES (?, ?)", (question, answer)
    )
    con.commit()
    return cur.rowcount == 1


def get_question_by_id(id):
    cur = con.cursor()
    cur.execute("SELECT * FROM questions WHERE id = ?", (id,))
    return cur.fetchone()


def insert_choice(question_id, choice) -> bool:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO choices (question_id, answer) VALUES (?, ?)", (question_id, choice)
    )
    con.commit()
    return cur.rowcount == 1


def get_choice_by_id(id):
    cur = con.cursor()
    cur.execute("SELECT * FROM choices WHERE id = ?", (id,))
    return cur.fetchone()
