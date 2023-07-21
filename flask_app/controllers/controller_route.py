from flask import render_template, request, redirect, session
from flask_app import app

# Landing on main page
@app.route('/')
def home():
    if 'user_id' not in session:
        return render_template('access.html')
    return redirect ('/recipes')