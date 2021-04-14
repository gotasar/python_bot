import psycopg2


class DB:
    conn = None

    @staticmethod
    def get():
        if DB.conn is None:
            DB.conn = psycopg2.connect(database="dfh4u9ku9r591a",
                                       user="pihbteuhurzhje",
                                       password="0318a7704a9234b8744cba962b1b1a63b919d5a87d4810b4810f299794749ae8",
                                       host="ec2-52-71-161-140.compute-1.amazonaws.com",
                                       port=5432)
        return DB.conn
