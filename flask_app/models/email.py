from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Email:
    db = "email_validation"
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO emails (email) VALUES (%(email)s);"
        return connectToMySQL('email_schema').query_db( query, data )

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL('email_schema').query_db(query)
        emails = []
        for email in results:
            emails.append( cls(email) )
        return emails

    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL('email_schema').query_db(query,data)

    @staticmethod
    def is_valid(email):
        is_valid = True
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        results = connectToMySQL('email_schema').query_db(query,email)
        if len(results) >= 1:
            flash("Email address is already taken.")
            is_valid=False
        if not EMAIL_REGEX.match(email['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid