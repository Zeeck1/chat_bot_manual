import json
import os
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a real secret key

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = generate_password_hash('adminpassword')  # Replace with the actual password

# File path to store questions
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'questions.json')

# Load questions from file
def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, 'r') as f:
            return json.load(f)
    return []

# Save questions to file
def save_questions(questions):
    with open(QUESTIONS_FILE, 'w') as f:
        json.dump(questions, f, indent=4)

@app.route("/")
def home_route():
    return render_template("home.html")

@app.route("/chat", methods=["GET", "POST"])
def chat_route():
    questions = load_questions()  # Load questions from file
    if request.method == "POST":
        selected_question = request.form["question"]
        response = next((q["answer"] for q in questions if q["question"] == selected_question), "No answer found")
        return jsonify({"response": response})
    return render_template("chat.html", questions=questions)



@app.route("/admin", methods=["GET", "POST"])
def admin_route():
    if 'logged_in' not in session:
        return redirect(url_for('login_route'))
    if request.method == "POST":
        new_question = request.form["question"]
        new_answer = request.form["answer"]
        questions = load_questions()  # Load questions from file
        questions.append({"question": new_question, "answer": new_answer})
        save_questions(questions)  # Save updated questions to file
        return redirect(url_for("admin_route"))
    return render_template("admin.html")

@app.route("/login", methods=["GET", "POST"])
def login_route():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['logged_in'] = True
            return redirect(url_for("admin_route"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
def logout_route():
    session.pop('logged_in', None)
    return redirect(url_for("home_route"))

if __name__ == "__main__":
    app.run(debug=True)