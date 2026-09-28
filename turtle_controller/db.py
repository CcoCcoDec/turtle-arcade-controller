import pymysql


DB_CONFIG = {
    'host': 'localhost',
    'user': 'turtle_user',
    'password': '1234',
    'database': 'turtle_db',
    'charset': 'utf8mb4'
}


class Database:

    def __init__(self):

        self.connection = pymysql.connect(
            **DB_CONFIG
        )

    # ==================================================
    # Insert turtle data
    # ==================================================

    def insert_log(
        self,
        x,
        y,
        theta,
        action
    ):

        sql = """
        INSERT INTO turtle_log
        (x, y, theta, action)
        VALUES (%s, %s, %s, %s)
        """

        cursor = self.connection.cursor()

        cursor.execute(
            sql,
            (
                x,
                y,
                theta,
                action
            )
        )

        self.connection.commit()

        cursor.close()

    # ==================================================
    # Get turtle data
    # ==================================================

    def get_logs(self):

        sql = """
        SELECT
            id,
            x,
            y,
            theta,
            action,
            created_at
        FROM turtle_log
        ORDER BY id DESC
        """

        cursor = self.connection.cursor()

        cursor.execute(sql)

        result = cursor.fetchall()

        cursor.close()

        return result

    # ==================================================
    # Close connection
    # ==================================================

    def close(self):

        self.connection.close()