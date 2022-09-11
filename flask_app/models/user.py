from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app

from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

import re
from flask import flash


# FIRST_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# LAST_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    # could enter variable here and set it = to schema name in workbench
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.user_email = data['user_email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.pass_hash = data['pass_hash']

    @staticmethod
    def validate_user( user ):
        is_valid = True
        # validation for names and pass set to == 
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.")
            print('first_name flash')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.")
            print('last_name flash')
            is_valid = False
        if not EMAIL_REGEX.match(user['user_email']): 
            flash("Please use the correct email format")
            print('email flash')
            is_valid = False
        if len(user['pass_word']) < 8:
            flash("Password must be longer.")
            print('password flash')
            is_valid = False
        if user['pass_word'] != user['confirm_pass']:
            flash("Passwords do not match.")
            print('confirm password flash')
            is_valid = False
        # data = {
        #     'user_email': user['user_email']
        # }
        # # below we give request.form a variable user above in the arguement for this method
        # user_in_db = User.get_by_email(data)
        # # print(user_in_db)
        # if user_in_db:
        #     flash('Email already in database.')
        #     is_valid = False

        return is_valid

    @staticmethod
    def validate_login( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['user_email']): 
            flash("Email or Password incorrect")
            print('email flash')
            is_valid = False
        if len(user['passwo_rd']) == 8:
            flash("Email or Password incorrect")
            print('password flash')
            is_valid = False
        return is_valid

    # class method to save our dojo to the database
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name, last_name, user_email, password ) VALUES ( %(first_name)s , %(last_name)s, %(user_email)s, %(pass_word)s );"
        results = connectToMySQL('l_r_schema').query_db( query, data )
        # prints id of user
        print(results)
        return results

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('l_r_schema').query_db(query)
        users = []
        for one_user in results:
            users.append( cls(one_user) )
        print(users)
        return users

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id =%(id)s;"
        # data comes from session, storing it in varibale results
        results = connectToMySQL('l_r_schema').query_db(query, data )
        print(results)
        # returning back to controller file user instance of data returned from database
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE user_email =%(user_email)s;"
        results = connectToMySQL('l_r_schema').query_db(query, data )
        if results == False:
            return False
        return cls(results[0])
