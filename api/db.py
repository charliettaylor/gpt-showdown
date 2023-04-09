import sqlite3
from .schema import CreateQuestion, CreateChoice
from .schema import Question

con = sqlite3.connect("qc.db")
con.row_factory = sqlite3.Row

QUIZZES = "CREATE TABLE IF NOT EXISTS quizzes (id INTEGER PRIMARY KEY, name TEXT)"
QUESTIONS = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, quiz_id INTEGER, question TEXT, answer TEXT)"
CHOICES = "CREATE TABLE IF NOT EXISTS choices (id INTEGER PRIMARY KEY, question_id INTEGER,choice TEXT, value TEXT)"


def create_schema():
    cur = con.cursor()
    cur.execute(QUIZZES)
    cur.execute(QUESTIONS)
    cur.execute(CHOICES)
    con.commit()


def insert_quiz(name: str) -> int | None:
    print("penis", name)
    cur = con.cursor()
    cur.execute("INSERT INTO quizzes (name) VALUES (?)", (name,))
    con.commit()
    return cur.lastrowid


def insert_question(quiz_id: int, q: CreateQuestion) -> int | None:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO questions (quiz_id, question, answer) VALUES (?, ?, ?)",
        (quiz_id, q.question, q.answer),
    )
    con.commit()
    return cur.lastrowid


def insert_choice(question_id: int, c: CreateChoice) -> int | None:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO choices (question_id, choice, value) VALUES (?, ?, ?)",
        (question_id, c.choice, c.value),
    )
    con.commit()

    return cur.lastrowid


def get_all_quizzes():
    cur = con.cursor()
    cur.execute("SELECT * FROM QUIZZES")
    rows = cur.fetchall()
    return rows


def get_questions_by_quiz(quiz_id: int) -> list[Question]:
    cur = con.cursor()

    cur.execute("SELECT * FROM questions WHERE quiz_id = ?", (str(quiz_id)))
    rows = cur.fetchall()
    return [Question(**x) for x in rows]


if __name__ == "__main__":
    rows = get_questions_by_quiz(1)
    for row in rows:
        print(row)
