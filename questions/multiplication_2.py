import json
import random

def load_questions():
    with open("questions/multiplication_2.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_random_question():
    questions = load_questions()
    return random.choice(questions)
