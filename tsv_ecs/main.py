#!/usr/bin/python3
import os
from flask import Flask

app = Flask(__name__)
import psycopg2


@app.route('/')
def hello_world():
    name = os.environ.get('NAME', 'World !!!')
    return 'Hello {}!'.format(name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',
                                                                8080)))


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host='rdsstack-databaseb269d8bb-qf7k4svkwmel.cluster-crvlivhlm5ax.eu-central-1.rds.amazonaws.com',
                             user='stara',
                             password='8C4Pi2WCZx%3',
                             database='postgres')

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version :')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        print("ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
