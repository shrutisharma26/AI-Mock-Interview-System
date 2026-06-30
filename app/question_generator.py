import random

from data.question_bank import QUESTION_BANK
from data.company_questions import COMPANY_QUESTIONS
from data.skill_questions import SKILL_BASED_QUESTIONS


def generate_questions(
        role,
        difficulty,
        company="General",
        num_questions=5
):

    if company != "General":

        questions = COMPANY_QUESTIONS.get(
            company,
            []
        )

        if len(questions) > 0:
            random.shuffle(questions)
            return questions[:num_questions]

    questions = QUESTION_BANK[role][difficulty]

    if len(questions) <= num_questions:
        return questions

    return random.sample(
        questions,
        num_questions
    )


def generate_skill_questions(
        skills,
        num_questions=5
):

    questions = []

    for skill in skills:

        if skill in SKILL_BASED_QUESTIONS:
            questions.extend(
                SKILL_BASED_QUESTIONS[skill]
            )

    if len(questions) == 0:
        return []

    random.shuffle(questions)

    return questions[:num_questions]