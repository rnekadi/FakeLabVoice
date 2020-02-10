import mysql.connector
from mysql.connector import Error


def create_connection():
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', database='fakelab', user='root', password='')
        print("Connected to MySQL")
    except Error as e:
        print("Error while connecting to MySQL", e)

    return conn


def create_prediction(conn, cur_inference):
    """
    Create a new experiment into the experiments table
    :param conn:
    :param project:
    :return: project id
    """
    data_tuple = (cur_inference.pred_id, cur_inference.user_id, cur_inference.time_stamp, cur_inference.prob
                  , cur_inference.stype)

    sql = ''' INSERT INTO `fake_voice` (pred_id,user_id,time_stamp,prob,stype) VALUES (%s, %s, %s, %s, %s); '''

    try:
        cur = conn.cursor()
        cur.execute(sql, data_tuple)
        conn.commit()
        return cur.lastrowid
        print(cur.rowcount, "Record inserted successfully into fake_voice table")
        cur.close()
    except mysql.connector.Error as error:
        print("Failed to insert record into fake_voice table {}".format(error))

    finally:
        if conn.is_connected():
            conn.close()
            print("MySQL connection is closed")
