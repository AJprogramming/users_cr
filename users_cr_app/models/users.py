from users_cr_app.conf.mysqlconnection import connectToMySQL
# model the class after the users table from our database
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
        VALUES ( %(session['first_name'])s , %(session['last_name'])s , %(session['email'])s , NOW() , NOW() )
        ;"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('users_schema').query_db( query, data )
    
    @classmethod
    def edit(cls, data):
        query = """UPDATE users 
        SET first_name=%(session['first_name'])s , last_name=%(session['last_name'])s, email=%(session['email'])s, updated_at=NOW()
        WHERE id = %(session['id'])s
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
