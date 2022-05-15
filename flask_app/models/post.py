# from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Post:
    database_name = 'blog'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.title = data['title']
        self.body = data['body']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (user_id, title, body, created_at, updated_at) VALUES (%(user_id)s, %(title)s, %(body)s, NOW(), NOW())"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        results = connectToMySQL(cls.database_name).query_db(query)
        print(results)
        all_posts = []
        for post in results:
            all_posts.append(cls(post))
        return all_posts

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        print(results)
        return cls(results[0])

    # @classmethod
    # def get_one_by_title(cls, data):
    #     query = "SELECT * FROM posts WHERE title = %(title)s;"
    #     results = connectToMySQL(cls.database_name).query_db(query, data)
    #     print(results)
    #     return cls(results[0])

    @classmethod
    def get_one_post_by_user(cls, data):
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        this_post = cls(results[0])
        user_data = {
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["created_at"],
            "updated_at": results[0]["updated_at"]
        }
        this_user = User(user_data)
        this_post.user = this_user
        return this_post

    @classmethod
    def get_all_posts_by_user(cls):
        query = "SELECT * FROM posts LEFT JOIN users ON posts.user_id = users.id;"
        results = connectToMySQL(cls.database_name).query_db(query)
        print(results)
        all_posts = []
        for post in results:
            user_data = {
                "id": post["users.id"],
                "first_name": post["first_name"],
                "last_name": post["last_name"],
                "email": post["email"],
                "password": post["password"],
                "created_at": post["users.created_at"],
                "updated_at": post["users.updated_at"]
            }
            these_users =  User(user_data)
            this_post = cls(post)
            this_post.user = these_users #Associate post with user by the post attribute which is the self.user created in constructor
            all_posts.append(this_post)
        return all_posts

    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET title=%(title)s, body=%(body)s, updated_at=NOW() WHERE id = %(id)s;"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # @classmethod
    # def update_by_title(cls, data):
    #     query = "UPDATE posts SET title=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE title = %(title)s;"
    #     results = connectToMySQL(cls.database_name).query_db(query, data)
    #     return results

    @classmethod
    def dunzo(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        results = connectToMySQL(cls.database_name).query_db(query, data)
        return results

    # @classmethod
    # def dunzo_by_title(cls, data):
    #     query = "DELETE FROM posts WHERE title = %(title)s"
    #     results = connectToMySQL(cls.database_name).query_db(query, data)
    #     return results

    @staticmethod
    def validate_post(form):
        is_valid = True
        if len(form['title']) < 5:
            flash("Title must be at least 5 characters.")
            is_valid = False
        if len(form['body']) < 10:
            flash("Body must be at least 10 characters.")
            is_valid = False
        return is_valid