import sqlite3
from .schema import CreateQuestion, CreateChoice

con = sqlite3.connect("qc.db")

QUIZZES = "CREATE TABLE IF NOT EXISTS quizzes (id INTEGER PRIMARY KEY, name TEXT)"
QUESTIONS = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, quiz_id INTEGER, question TEXT, answer TEXT)"
CHOICES = "CREATE TABLE IF NOT EXISTS choices (id INTEGER PRIMARY KEY, question_id INTEGER,choice TEXT)"


def create_schema():
    cur = con.cursor()
    cur.execute(QUIZZES)
    cur.execute(QUESTIONS)
    cur.execute(CHOICES)
    con.commit()


def insert_quiz(name: str) -> bool:
    print("penis", name)
    cur = con.cursor()
    cur.execute("INSERT INTO quizzes (name) VALUES (?)", (name,))
    con.commit()
    return cur.lastrowid


def insert_question(quiz_id: int, q: CreateQuestion) -> bool:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO questions (quiz_id, question, answer) VALUES (?, ?, ?)",
        (quiz_id, q.question, q.answer),
    )
    con.commit()
    return cur.lastrowid


def insert_choice(question_id: int, c: CreateChoice) -> bool:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO choices (question_id, choice) VALUES (?, ?)", (question_id, c.choice)
    )
    con.commit()

    return cur.lastrowid

