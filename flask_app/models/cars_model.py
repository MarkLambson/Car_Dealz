from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.sellers_model import Seller

class Car:
    DATABASE = 'carz_db'
    def __init__(self,data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.seller_id = data['seller_id']

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO cars (price, model, make, year, description, seller_id)
        VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(seller_id)s);
        """ 
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cars;"
        results =  connectToMySQL(cls.DATABASE).query_db(query)
        all_cars = []
        if results:
            for row in results:
                todo_cars = cls(row)
                all_cars.append(todo_cars)
        return all_cars

#this is where the join is-----------------------------------------------------------------------
    @classmethod
    def get_one_with_seller(cls,id):
        data ={'id' : id}
        query = """
            SELECT * FROM cars
            JOIN sellers ON
            cars.seller_id = sellers.id
            WHERE cars.id = %(id)s
            ;
        """
        results =  connectToMySQL(cls.DATABASE).query_db(query,data)
        if results:
            row = results[0]
            car = cls(row)
            seller_data = {
                "id" : row['sellers.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['sellers.created_at'],
                "updated_at" : row['sellers.updated_at']
                }
            seller = Seller(seller_data)
            car.creator = seller
            return car
#this is where the join ends---------------------------------------------------------------

#this is another join for dashboard--------------------------------------------------------
    @classmethod
    def get_all_with_sellers(cls):
        query = """
        SELECT * FROM cars
        JOIN sellers ON
        cars.seller_id = sellers.id;
        """
        results =  connectToMySQL(cls.DATABASE).query_db(query)
        sellers = []
        if results:
            for row in results:
                car = cls(row)
                seller_data = {
                    "id" : row['sellers.id'],
                    "first_name" : row['first_name'],
                    "last_name" : row['last_name'],
                    "email" : row['email'],
                    "password" : row['password'],
                    "created_at" : row['sellers.created_at'],
                    "updated_at" : row['sellers.updated_at']
                }
                seller = Seller(seller_data)
                car.owner = seller
                sellers.append(car)
        print(sellers)
        return sellers


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM cars WHERE id = %(id)s;"
        results = connectToMySQL(cls.DATABASE).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = """UPDATE cars SET 
            price=%(price)s, model=%(model)s, make=%(make)s,
            year=%(year)s, description=%(description)s 
            WHERE id = %(id)s;
            """
        return connectToMySQL(cls.DATABASE).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.DATABASE).query_db(query,data)

    @staticmethod
    def validate_car(car):
        is_valid = True
        if int(car['price']) < 1:
            is_valid = False
            flash("Price is required and must be greater than 0","car")
        if len(car['model']) < 2:
            is_valid = False
            flash("Model name is required and must be at least 2 characters","car")
        if len(car['make']) < 1:
            is_valid = False
            flash("Make is required and must be at least 1 character","car")
        if int(car['year']) < 1:
            is_valid = False
            flash("Year is required and must be greater than 0","car")
        if len(car['description']) < 3:
            is_valid = False
            flash("Description is required and must be at least 3 characters","car")
        return is_valid