from pydantic import BaseModel


class QuizBase(BaseModel):
    name: str


class Quiz(QuizBase):
    id: int


class ChoiceBase(BaseModel):
    choice: str
    value: str


class Choice(ChoiceBase):
    id: int
    question_id: int


class CreateChoice(ChoiceBase):
    pass


class QuestionBase(BaseModel):
    question: str
    answer: str


class Question(QuestionBase):
    id: int
    quiz_id: int


class CreateQuestion(QuestionBase):
    choices: list[CreateChoice]


class CreateQuiz(QuizBase):
    questions: list[CreateQuestion]
