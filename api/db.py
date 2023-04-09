import sqlite3
from .schema import (
    CreateQuestion,
    CreateChoice,
    CreateQuiz,
    McQuestion,
    Question,
    ChoiceBase,
)

con = sqlite3.connect("qc.db")
con.row_factory = sqlite3.Row

QUIZZES = "CREATE TABLE IF NOT EXISTS quizzes (id INTEGER PRIMARY KEY, name TEXT, category TEXT)"
QUESTIONS = "CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, quiz_id INTEGER, question TEXT, answer TEXT)"
CHOICES = "CREATE TABLE IF NOT EXISTS choices (id INTEGER PRIMARY KEY, question_id INTEGER,choice TEXT, value TEXT)"


def create_schema():
    cur = con.cursor()
    cur.execute(QUIZZES)
    cur.execute(QUESTIONS)
    cur.execute(CHOICES)
    con.commit()


def insert_quiz(quiz: CreateQuiz) -> int | None:
    cur = con.cursor()
    cur.execute(
        "INSERT INTO quizzes (name, category) VALUES (?, ?)", (quiz.name, quiz.category)
    )
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


def get_choices_by_question(question_id: int):
    cur = con.cursor()
    cur.execute("SELECT * FROM choices WHERE question_id = ?", (str(question_id)))
    rows = cur.fetchall()
    return rows


def get_questions_by_quiz(quiz_id: int) -> list[McQuestion]:
    things = []

    cur = con.cursor()

    cur.execute("SELECT * FROM questions WHERE quiz_id = ?", (str(quiz_id)))
    rows = cur.fetchall()

    for row in rows:
        choices = get_choices_by_question(row["id"])
        things.append(
            McQuestion(
                question=row["question"], choices=[ChoiceBase(**x) for x in choices]
            )
        )

    return things


def get_all_quiz_categories():
    cur = con.cursor()
    cur.execute("SELECT DISTINCT category FROM QUIZZES")
    rows = cur.fetchall()
    return rows


if __name__ == "__main__":
    rows = get_questions_by_quiz(1)
    for row in rows:
        print(row)
