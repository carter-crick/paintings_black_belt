from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.model_painting import Painting
from flask_app.models.model_user import User

# Display all Paintings
@app.route('/paintings')
def paintings():
    paintings = Painting.get_all()
    user_paintings = Painting.get_all_owned(session['user_id'])
    user = User.get_by_id({'id': session['user_id']})
    return render_template('paintings.html', paintings=paintings, user_paintings=user_paintings, user=user)

# Display Form to Create Painting
@app.route('/paintings/new', methods=['GET'])
def new_painting():
    return render_template('add_painting.html')

# Process Form to Create Painting
@app.route('/paintings/create', methods=['POST'])
def create_painting():
    data = {**request.form}
    if not Painting.validate_painting(data):
        print("IF NOT")
        return redirect('/paintings/new')
    print("BEFORE CREATE")
    Painting.create(data)
    return redirect('/paintings')

# Display One Painting
@app.route('/paintings/view/<int:painting_id>')
def show_painting(painting_id):
    painting = Painting.get_by_id({'id': painting_id})
    return render_template('view_painting.html', painting=painting)

# Display Form to Edit Painting
@app.route('/paintings/edit/<int:painting_id>')
def edit_painting(painting_id):
    if not Painting.created_by_user({'painting_id': painting_id, 'user_id': session['user_id']}):
        return redirect('/paintings')
    painting = Painting.get_by_id({'id': painting_id})
    return render_template('edit_painting.html', painting=painting)

# Process Form to Update Painting
@app.route('/paintings/update/<int:painting_id>', methods=['POST'])
def update_painting(painting_id):
    data = {**request.form}
    data['id'] = painting_id
    if not Painting.validate_painting(request.form):
        return redirect(f'/paintings/edit/{painting_id}')
    Painting.update_painting(data)
    print('*' * 100)
    print(data)
    return redirect('/paintings')

# Delete Painting
@app.route('/paintings/delete/<int:painting_id>')
def delete_painting(painting_id):
    if not Painting.created_by_user({'painting_id': painting_id, 'user_id': session['user_id']}):
        return redirect('/paintings')
    print('*' * 100)
    print(painting_id)
    Painting.delete_painting(painting_id)
    return redirect('/paintings')

#Buy Painting
@app.route('/paintings/buy/<int:painting_id>', methods=['POST'])
def buy_painting(painting_id):
    print("buy route hit")
    data = {'user_id': session['user_id'], 'painting_id': painting_id}
    Painting.buy(data)
    print(data)
    return redirect('/paintings')