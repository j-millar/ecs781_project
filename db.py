import requests
import coinsentiment
import pandas as pd
import datetime
import pymysql
from flask import jsonify
import os
import sqlalchemy


db_un = "root"
db_pw = "nhAkiDy1FNaLmlxA"
db_cname = "eternal-bruin-341420:europe-west1:coininfo"
db_name = "test"
db_ip = "35.205.39.188"

def open_connection():
	url = "mysql+pymysql://{}:{}@{}/{}?unix_socket=/cloudsql/{}".format(
		db_un, 
		db_pw,
		db_ip, 
		db_name,
		db_cname
		)

	engine = sqlalchemy.create_engine(
		sqlalchemy.engine.url.URL(
			host=db_ip,
			drivername="mysql+pymysql", 
			username=db_un,
			password=db_pw, 
			database=db_name, 
			query={
				"unix_socket": "/cloudsql/{}".format(db_cname)
			}
		),
	)

	try:
		conn = engine.connect()

	except pymysql.MySQLError as e:
		print(e)
	return conn

def getcoins():
	conn = open_connection()
	print(conn)	
	with conn.cursor() as cursor:
		result = cursor.execute("SELECT * FROM coins;")
		coins = cursor.fetchall()
		if result > 0:
			got_coins = jsonify(coins)
		else:
			got_coins = "database empty"
	conn.close()
	return got_coins

def add_coins(coin):
	conn = open_connection()
	with conn.cursor as cursor:
		cursor.execute("INSERT INTO coins (coinname, cointicker, price, popularity, sentiment) VALUES(%s, %s, %f, %f, %f)",
			(coin["name"], coin["ticker"], coin["price"], coin["popularity"], coin["sentiment"]))

	conn.commit()
	conn.close
