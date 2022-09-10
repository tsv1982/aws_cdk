#!/usr/bin/python3
import os
from flask import Flask
app = Flask(__name__)
import psycopg2

import pymysql

host = 'admin.cjp8hsqu4je0.us-east-2.rds.amazonaws.com'
user = 'admin'
password = '12345678'
database = 'admin'

connection = pymysql.connect(host='database-5.cgfwgn6bvnum.eu-central-1.rds.amazonaws.com',
                             user='admin',
                             password='zxzxzx123',
                             database='database-5')
with connection:
    cur = connection.cursor()
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print("Database version: {} ".format(version[0]))



@app.route('/')
def hello_world():
    name = os.environ.get('NAME', 'World')
    return 'Hello {}!'.format(name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',
            8080)))
