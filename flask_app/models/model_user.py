from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE, bcrypt, EMAIL_REGEX, PASSWORD_REGEX, NAME_REGEX

# Create your models here.
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.hashed_password = data['hashed_password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result[0]:
            return cls(result[0])
        else:
            return False

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result:
            return cls(result[0])
        else:
            return False

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name,last_name,email,hashed_password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(hashed_password)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters", "error_users_first_name")
            print("fname")
            is_valid = False
            
        if not NAME_REGEX.match(data['first_name']):
            flash("First name must contain only characters", "error_users_first_name")
            print("fname2")
            is_valid = False

        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters", "error_users_last_name")
            print("lname")
            is_valid = False

        if not NAME_REGEX.match(data['first_name']):
            flash("Last name must contain only characters", "error_users_last_name")
            print("lname2")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email", "error_users_email")
            print("email")
            is_valid = False

        if User.get_by_email(data):
            flash("Email already exists", "error_users_email")
            print("email2")
            is_valid = False

        if data['password'] != data['confirm_password']:
            flash("Passwords must match", "error_users_hashed_password")
            print("pword")
            is_valid = False

        if not PASSWORD_REGEX.match(data['password']):
            flash("Passwords need Capital letter, Special Character, and Number", "error_users_password")
            print("pword2")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        user_data = User.get_by_email(data)
        if user_data:
            print ('*' * 100)
            print (data['password'])
            if not bcrypt.check_password_hash(user_data.hashed_password, data['password']):
                flash("Incorrect password", "error_users_password_login")
                is_valid = False
        else:
            flash("Email not registered", "error_users_email_login")
            is_valid = False
        return is_valid