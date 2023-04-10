import re
from collections import defaultdict
from ..schema import CreateQuiz, CreateQuestion, CreateChoice
from ..db import create_schema, insert_quiz, insert_choice, insert_question


def insert_quizzes():
    input_file = open("quizzes/default-quizzes.txt")
    raw = input_file.read()
    categories = [x[:-1] for x in re.findall(r".+:", raw) if "Answer" not in x]
    questions = re.findall(r"\d\. .*", raw)

    choices = re.findall(r"[A-Z]\).*", raw)
    assert len(choices) == len(questions) * 5, "Improper Choice to Question ratio"

    category_to_questions: dict[str, list[str]] = defaultdict(lambda: list())
    category = -1
    actual_choices = []
    answers = []
    for i, question in enumerate(questions):
        if "1." in question:
            category += 1
            # go next category
        category_to_questions[categories[category]].append(question)
        raw_choices = choices[i * 5 : i * 5 + 4]
        correct_choice = choices[i * 5 + 4]
        answers.append(correct_choice)
        for choice in raw_choices:
            actual_choices.append(CreateChoice(choice=choice[0], value=choice[3:]))

    quizzes = []
    # print(choices)
    # print(answers)
    # print(len(answers))
    print(actual_choices)
    # print(len(questions), " ", (len(actual_choices)))

    for cidx, category in enumerate(categories):
        quiz_name = category.lower() + "-1"
        questions_for_category = category_to_questions[category]
        answer_for_questions = [
            answers[i][0] for i in range(len(questions_for_category))
        ]
        choices_for_question = [
            actual_choices[i * 4 : i * 4 + 4]
            for i in range(len(questions_for_category))
        ]

        # print(
        #     f"{questions_for_category=}, {answer_for_questions=}, {choices_for_question}\n"
        # )
        questions_list = []
        for i, _question in enumerate(questions_for_category):
            new_question = CreateQuestion(
                question=_question,
                answer=answer_for_questions[i][0],
                choices=choices_for_question[i],
            )
            questions_list.append(new_question)

        quiz = CreateQuiz(name=quiz_name, category=category, questions=questions_list)
        quiz_id = insert_quiz(quiz)

        # print(questions_list)
        for i, _question in enumerate(questions_list):
            question_id = insert_question(quiz_id=quiz_id, q=_question)
            for choice in choices_for_question[i]:
                insert_choice(question_id=question_id, c=choice)

    return quizzes


if __name__ == "__main__":
    create_schema()
    quizzes = insert_quizzes()
    # print(quizzes)
