from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Show:
    db = "tv_shows"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def get_all(cls, user_id):
        query = "SELECT * FROM shows LEFT JOIN users on shows.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        shows = []
        for show in results:
            added_by_current_user = show['user_id'] == user_id
            show['added_by_current_user'] = added_by_current_user
            shows.append( show )
        return shows

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO shows (title , network , release_date , description, created_at, updated_at, user_id) VALUES ( %(title)s , %(network)s , %(release_date)s , %(description)s , NOW() , NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db( query, data )

    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM shows WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def is_valid_show(show):
        is_valid = True

        if len(show["title"]) <= 0:
            is_valid = False
            flash("Title is required.")
        if len(show["title"]) <= 2:
            is_valid = False
            flash("Title must be at least 3 characters.")
        if len(show["network"]) <= 0:
            is_valid = False
            flash("Network is required.")
        if len(show["network"]) <= 2:
            is_valid = False
            flash("Network must be at least 3 characters.")
        if len(show["description"]) <= 0:
            is_valid = False
            flash("Description is required.")
        if len(show["description"]) <= 2:
            is_valid = False
            flash("Description must be at least 3 characters.")
        if len(show["release_date"]) <= 0:
            is_valid = False
            flash("Release date is required.")
        return is_valid

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM shows LEFT JOIN users on shows.user_id = users.id WHERE shows.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results[0]