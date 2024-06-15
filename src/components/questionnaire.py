from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your own secret key
# Supabase configuration
SUPABASE_URL = 'https://zqxdgopzsaoyhctnghaa.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpxeGRnb3B6c2FveWhjdG5naGFhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY1NjkzNDEsImV4cCI6MjAzMjE0NTM0MX0.2kOPWjNeeEQQyXzfC_ORHOV1UZMoNXJg5pYOPoKlUgM'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('questionnaire'))
    return render_template('index.html')

@app.route('/sign_up', methods=['POST'])
def sign_up():
    email = request.form['email']
    password = request.form['password']
    response = supabase.auth.sign_up({'email': email, 'password': password})
    if 'error' in response:
        return jsonify({"error": response['error']['message']}), 400
    if 'data' in response and 'user' in response['data']:
        session['user'] = response['data']['user']
        return redirect(url_for('questionnaire'))
    else:
        return jsonify({"error": "Invalid response from Supabase"}), 400

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
    if 'error' in response:
        return jsonify({"error": response['error']['message']}), 400
    if 'data' in response and 'user' in response['data']:
        session['user'] = response['data']['user']
        return redirect(url_for('questionnaire'))
    else:
        return jsonify({"error": "Invalid response from Supabase"}), 400

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/questionnaire')
def questionnaire():
    # if 'user' not in session:
    #     return redirect(url_for('index'))
    return render_template('survey.html')

@app.route('/next_question', methods=['POST'])
def next_question():
    current_answers = request.json
    next_q = get_next_question(current_answers)
    return jsonify(next_q)

def get_next_question(answers):
    if not answers:
        return {"question": "What is your name?", "options": [], "key": "name"}
    # Your logic for determining the next question based on answers goes here

def save_to_supabase(data):
    supabase.table('survey_responses').insert(data).execute()

if __name__ == '__main__':
    app.run(debug=True)
