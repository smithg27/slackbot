import pymysql
from peewee import *
import os
import settings

db = MySQLDatabase(host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")), user=os.environ.get("DB_USER"), passwd=os.environ.get("DB_PASS"), database=os.environ.get("DB_DATABASE"))