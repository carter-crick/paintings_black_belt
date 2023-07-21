from flask import render_template, request, redirect, session
from flask_app import app, bcrypt
from flask_app.models.model_user import User

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        print("if not")
        return redirect('/')
    hash_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {**request.form}
    data['hashed_password'] = hash_pass
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/paintings')

@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    user_in_db = User.get_by_email(request.form)

    session['user_id'] = user_in_db.id
    return redirect('/paintings')


# User Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')

# Display User Profile
@app.route('/users/<int:user_id>', methods=['GET'])
def profile(user_id):
    user = User.get_by_id({'id': user_id})
    return render_template('profile.html', user=user)