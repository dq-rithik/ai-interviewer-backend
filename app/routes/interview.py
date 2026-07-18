from flask import Blueprint, request, jsonify
from app.services.interview_service import generate_interview_questions
from app.services.evaluation_service import evaluate_completed_interview

interview_bp = Blueprint('interview', __name__)

@interview_bp.route('/interview/generate', methods=['POST'])
def generate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body."}), 400
        
    # Extract fields
    fullName = data.get("fullName")
    jobRole = data.get("jobRole")
    experienceLevel = data.get("experienceLevel")
    skills = data.get("skills")
    interviewType = data.get("interviewType")
    difficulty = data.get("difficulty")
    numQuestions = data.get("numQuestions")
    
    # Validation
    errors = {}
    if not fullName or not isinstance(fullName, str) or not fullName.strip():
        errors["fullName"] = "Full name is required and must be a string."
    if not jobRole or not isinstance(jobRole, str) or not jobRole.strip():
        errors["jobRole"] = "Job role is required and must be a string."
    if experienceLevel not in ["Fresher", "Experienced"]:
        errors["experienceLevel"] = "Experience level must be 'Fresher' or 'Experienced'."
    if not skills or not isinstance(skills, list) or len(skills) == 0:
        errors["skills"] = "Skills must be a non-empty list of strings."
    if interviewType not in ["HR", "Technical", "Mixed"]:
        errors["interviewType"] = "Interview type must be 'HR', 'Technical', or 'Mixed'."
    if difficulty not in ["Easy", "Medium", "Hard"]:
        errors["difficulty"] = "Difficulty must be 'Easy', 'Medium', or 'Hard'."
    
    try:
        num_q = int(numQuestions)
        if num_q < 1 or num_q > 15:
            errors["numQuestions"] = "Number of questions must be between 1 and 15."
    except (ValueError, TypeError):
        errors["numQuestions"] = "Number of questions must be an integer."
        
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
        
    profile = {
        "fullName": fullName.strip(),
        "jobRole": jobRole.strip(),
        "experienceLevel": experienceLevel,
        "skills": [s.strip() for s in skills if isinstance(s, str) and s.strip()]
    }
    
    config = {
        "interviewType": interviewType,
        "difficulty": difficulty,
        "numQuestions": num_q
    }
    
    try:
        questions = generate_interview_questions(profile, config)
        return jsonify({
            "status": "success",
            "profile": profile,
            "config": config,
            "questions": questions
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to generate interview questions.",
            "message": str(e)
        }), 500

@interview_bp.route('/interview/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body."}), 400
        
    user_profile = data.get("userProfile")
    config = data.get("config")
    questions = data.get("questions")
    answers = data.get("answers")
    
    # Basic structural validation
    errors = {}
    if not user_profile or not isinstance(user_profile, dict):
        errors["userProfile"] = "Missing or invalid user profile data."
    if not config or not isinstance(config, dict):
        errors["config"] = "Missing or invalid interview configuration."
    if not questions or not isinstance(questions, list):
        errors["questions"] = "Missing or invalid questions list."
    if answers is None or not isinstance(answers, dict):
        errors["answers"] = "Missing or invalid candidate answers."
        
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400
        
    try:
        report = evaluate_completed_interview(user_profile, config, questions, answers)
        return jsonify({
            "status": "success",
            "report": report
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to evaluate interview answers.",
            "message": str(e)
        }), 500
