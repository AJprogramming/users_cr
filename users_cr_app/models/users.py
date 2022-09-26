from users_cr_app.conf.mysqlconnection import connectToMySQL
from flask import flash
import re

email_validation = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_schema').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def save(cls, data ):
        query = """INSERT INTO users ( first_name , last_name , email , created_at, updated_at )
        VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() )
        ;"""
        return connectToMySQL('users_schema').query_db( query, data )
    
    @classmethod
    def edit(cls, data):
        query = """UPDATE users 
        SET first_name=%(first_name)s , last_name=%(last_name)s, email=%(email)s, updated_at=NOW()
        WHERE id = %('id')s
        ;"""
        results = connectToMySQL('users_schema').query_db(query, data)
        print("results", results)
        return results
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        result = connectToMySQL('users_schema').query_db(query, data)
        return cls(result[0])
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('users_schema').query_db(query,data)
    
    @staticmethod
    def validate(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "First Name")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "Last Name")
            is_valid = False
        if not email_validation.match(user['email']):
            flash("Invalid email address!", "Email:")
            is_valid = False
        return is_valid