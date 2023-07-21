from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE
from flask_app.models import model_user

class Painting:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.quantity = data['quantity']
        self.number_purchased = data['number_purchased']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO paintings (title, description, price, quantity, user_id) 
            VALUES (%(title)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def update_painting(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, quantity=%(quantity)s WHERE id=%(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM paintings JOIN users ON users.id = paintings.user_id LEFT JOIN users_has_paintings ON paintings.id = users_has_paintings.painting_id WHERE paintings.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []
        painting_data = results[0]
        painting_instance = cls(painting_data)
        users_data = {
            **painting_data,
            'id' : painting_data['users.id'],
            'created_at' : painting_data['users.created_at'],
            'updated_at' : painting_data['users.updated_at']
        }
        user_instance = model_user.User(users_data)
        painting_instance.user = user_instance
        if 'users_has_paintings.user_id' in painting_data and painting_data['users_has_paintings.user_id'] == session['user_id']:
            painting_instance.is_owned = True
        else:
            painting_instance.is_owned = False
        return painting_instance

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings JOIN users ON paintings.user_id = users.id LEFT JOIN users_has_paintings ON paintings.id = users_has_paintings.painting_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        
        if not results:
            return []

        paintings_list = []
        for painting in results:
            # changed from painting_object = cls([painting])
            painting_object = cls(painting)
            users_data = {
                **painting,
                'id' : painting['users.id'],
                'created_at' : painting['users.created_at'],
                'updated_at' : painting['users.updated_at']
            }
            user_instance = model_user.User(users_data)
            painting_object.user = user_instance
            if 'users_has_paintings.user_id' in painting and painting['users_has_paintings.user_id'] == session['user_id']:
                painting_object.is_owned = True
            else:
                painting_object.is_owned = False
            paintings_list.append(painting_object)
        return paintings_list
    
    @classmethod
    def get_all_owned(cls, user_id):
        query = """
            SELECT * 
            FROM paintings 
            JOIN users ON paintings.user_id = users.id 
            JOIN users_has_paintings ON paintings.id = users_has_paintings.painting_id
            WHERE users_has_paintings.user_id = %(user_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, {'user_id': user_id})
        
        if not results:
            return []

        paintings_list = []
        for painting in results:
            painting_object = cls(painting)
            users_data = {
                **painting,
                'id' : painting['users.id'],
                'created_at' : painting['users.created_at'],
                'updated_at' : painting['users.updated_at']
            }
            user_instance = model_user.User(users_data)
            painting_object.user = user_instance
            if 'users_has_paintings.user_id' in painting and painting['users_has_paintings.user_id'] == user_id:
                painting_object.is_owned = True
            else:
                painting_object.is_owned = False
            paintings_list.append(painting_object)
        return paintings_list

    @classmethod
    def created_by_user(cls, data):
        query = """
            SELECT * FROM paintings WHERE id = %(painting_id)s AND user_id = %(user_id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return True
        else:
            return False

    @classmethod
    def delete_painting(cls, id):
        print('*' * 100)
        print(id)
        query = "DELETE FROM paintings WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, {'id': id})
    
    @classmethod
    def buy(cls, data):
        add_owned = "INSERT INTO users_has_paintings (user_id, painting_id) VALUES (%(user_id)s, %(painting_id)s);"
        connectToMySQL(DATABASE).query_db(add_owned, data)

        inc_num_purchased = " UPDATE paintings SET number_purchased = number_purchased + 1 WHERE id = %(painting_id)s;"
        return connectToMySQL(DATABASE).query_db(inc_num_purchased, data)

    @staticmethod
    def validate_painting(data):
        print("*" * 100)
        print("hit valid")
        is_valid = True
        if len(data['title']) < 3:
            flash("Painting title must be at least 3 characters", "error_painting_title")
            is_valid = False
        if len(data['description']) < 10:
            flash("Description must be at least 10 characters", "error_painting_description")
            is_valid = False
        if not data['price']:
            flash("How much does it cost?", "error_painting_price")
            is_valid = False
        if not data['quantity']:
            flash("How many are there?", "error_painting_quantity")
            is_valid = False
        return is_valid