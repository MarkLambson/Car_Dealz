from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Seller:
    DATABASE = "carz_db"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls,data):
        query = """
            INSERT INTO sellers (first_name,last_name,email,password) 
            VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)
            """
        print(Seller)
        return connectToMySQL(cls.DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sellers;"
        results = connectToMySQL(cls.DATABASE).query_db(query)
        sellers = []
        if results:
            for row in results:
                sellers.append( cls(row))
        return sellers

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM sellers WHERE email = %(email)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM sellers WHERE id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(seller):
        is_valid = True
        query = "SELECT * FROM sellers WHERE email = %(email)s;"
        results = connectToMySQL(Seller.DATABASE).query_db(query,seller)
        if len(results) >= 1:
            flash("Email already taken","register")
            is_valid=False
        if not EMAIL_REGEX.match(seller['email']):
            flash("Invalid Email","register")
            is_valid=False
        if len(seller['first_name']) < 3:
            flash("First name must be at least 3 characters","register")
            is_valid= False
        if len(seller['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid= False
        if len(seller['password']) < 8:
            flash("Password must be at least 8 characters","register")
            is_valid= False
        if seller['password'] != seller['confirm_password']:
            flash("Passwords don't match","register")
            is_valid= False
        return is_valid