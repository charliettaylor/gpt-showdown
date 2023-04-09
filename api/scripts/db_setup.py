import re
from collections import defaultdict
from ..schema import CreateQuiz, CreateQuestion, CreateChoice
from ..db import create_schema, insert_quiz, insert_choice, insert_question


def insert_quizzes():
    input_file = open("quizzes/default-quizzes.txt")
    raw = input_file.read()
    categories = [x[:-1] for x in re.findall(r".+:", raw) if "Answer" not in x]
    questions = re.findall(r"\d\. .*", raw)

    category_to_questions: dict[str, list[str]] = defaultdict(lambda: list())
    category = -1
    for question in questions:
        if "1." in question:
            category += 1
            # go next category
        category_to_questions[categories[category]].append(question)

    choices = re.findall(r"[A-Z]\).*", raw)
    assert len(choices) == len(questions) * 5, "Improper Choice to Question ratio"

    quizzes = []
    # print(choices)
    for i, category in enumerate(categories):
        quiz_name = category.lower() + "-1"
        # print(i, category)
        answer = choices[(i * 5) + 4][0]
        raw_choices = choices[i * 4 : i * 4 + 4]
        actual_choices = []
        for choice in raw_choices:
            actual_choices.append(CreateChoice(choice=choice[0], value=choice[3:]))

        question_list = [
            CreateQuestion(question=x, answer=answer, choices=actual_choices)
            for x in category_to_questions[category]
        ]

        quiz = CreateQuiz(name=quiz_name, category=category, questions=question_list)
        quizzes.append(quiz)
        quiz_id = insert_quiz(quiz)
        assert quiz_id is not None, "Error: Invalid Quiz ID"

        for question_to_add in question_list:
            question_id = insert_question(quiz_id=quiz_id, q=question_to_add)
            assert question_id is not None, "Error: invalid question_id"
            for choice in actual_choices:
                insert_choice(question_id=question_id, c=choice)

    return quizzes


if __name__ == "__main__":
    create_schema()
    quizzes = insert_quizzes()
    # print(quizzes)
    for quiz in quizzes:
        print(quiz)
