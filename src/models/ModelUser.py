from .entities.User import User

class ModelUser():

    @classmethod
    def login(cls, db, username, password):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT * FROM users WHERE username = %s'

            cursor.execute(sql, (username,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                password = User.check_password(row[2], password)

                user = User(id, username, password)

                return user
            else:
                return None

        except Exception as e:

            raise Exception(e)


    @classmethod
    def get_by_id(cls, db, id):

        try:
            cursor = db.connection.cursor()
            sql = 'SELECT id, username FROM users WHERE id = %s'

            cursor.execute(sql, (id,))
            row = cursor.fetchone()

            if row:
                id = row[0]
                username = row[1]
                logged_user = User(id, username, None)

                return logged_user
            else:
                return None

        except Exception as e:

            raise Exception(e)