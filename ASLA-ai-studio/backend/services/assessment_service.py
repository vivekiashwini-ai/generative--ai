import json
from typing import List, Dict, Any
from pathlib import Path

# Question banks for different skills and difficulty levels
QUESTION_BANKS = {
    "Python": {
        "beginner": [
            {
                "id": 1,
                "question": "What is the correct way to define a function in Python?",
                "options": ["def my_function():", "function my_function():", "def my_function(x):", "function my_function(x)"],
                "answer": 0,
                "explanation": "In Python, functions are defined using the 'def' keyword followed by the function name and parentheses."
            },
            {
                "id": 2,
                "question": "Which of the following is used to iterate over a range of numbers?",
                "options": ["for i in range(5):", "for i from 0 to 5:", "for i in 5:", "for i = 0; i < 5; i++"],
                "answer": 0,
                "explanation": "The 'range()' function generates a sequence of numbers, and 'for i in range(5):' iterates over it."
            }
        ],
        "intermediate": [
            {
                "id": 1,
                "question": "What does the *args syntax do in a function?",
                "options": ["Returns the argument count", "Passes a variable number of non-keyword arguments", "Passes a variable number of keyword arguments", "Unpacks a dictionary"],
                "answer": 1,
                "explanation": "*args allows a function to accept a variable number of non-keyword arguments as a tuple."
            }
        ],
        "advanced": [
            {
                "id": 1,
                "question": "What is a decorator in Python?",
                "options": ["A function that modifies another function's behavior", "A syntax error", "A type of loop", "A built-in module"],
                "answer": 0,
                "explanation": "A decorator is a function that modifies the behavior of another function without changing its source code, using the '@decorator_name' syntax."
            }
        ]
    },
    "SQL": {
        "beginner": [
            {
                "id": 1,
                "question": "Which SQL clause is used to filter results?",
                "options": ["SELECT", "FROM", "WHERE", "GROUP BY"],
                "answer": 2,
                "explanation": "The WHERE clause is used to filter records based on specified conditions."
            }
        ],
        "intermediate": [],
        "advanced": []
    }
}

def start_assessment(skill: str, difficulty: str) -> Dict[str, Any]:
    """Start a skill assessment with questions"""
    bank = QUESTION_BANKS.get(skill, {}).get(difficulty, [])
    
    if not bank:
        return {
            "assessment_id": f"{skill.lower()}-{difficulty}-123",
            "skill": skill,
            "difficulty": difficulty,
            "questions": [],
            "total_questions": 0
        }
    
    return {
        "assessment_id": f"{skill.lower()}-{difficulty}-123",
        "skill": skill,
        "difficulty": difficulty,
        "questions": bank,
        "total_questions": len(bank)
    }

def submit_assessment(assessment_id: str, answers: Dict[str, int]) -> Dict[str, Any]:
    """Submit assessment answers and calculate score"""
    # Extract skill and total questions from assessment_id
    parts = assessment_id.split("-")
    skill = parts[0] if parts else ""
    total_questions = answers.get("_total", 0)
    
    # Calculate correct answers
    correct = 0
    for question_id, selected_answer in answers.items():
        if question_id.startswith("_"):
            continue
        if question_id.isdigit():
            q_index = int(question_id)
            if q_index < len(QUESTION_BANKS.get(skill, {}).get("beginner", [])):
                correct += 1  # Simplified: assume all answers are correct for demo
    
    percentage = round((correct / total_questions) * 100) if total_questions > 0 else 0
    
    # Generate topic analysis
    topic_analysis = {}
    if skill == "Python":
        topic_analysis = {"syntax": min(90, percentage + 10),
                         "functions": min(85, percentage + 5),
                         "libraries": max(0, percentage - 10)}
    elif skill == "SQL":
        topic_analysis = {"queries": percentage,
                         "joins": max(0, percentage - 15),
                         "aggregation": max(0, percentage - 20)}
    
    return {
        "assessment_id": assessment_id,
        "score": percentage,
        "correct_answers": correct,
        "total_questions": total_questions,
        "topic_analysis": topic_analysis,
        "feedback": f"Great job! You scored {percentage}%. Keep practicing to improve."
    }