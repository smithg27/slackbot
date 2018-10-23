from models import BeerScore
from models import UserGroup
from models import User
from peewee import *
import ../settings
import os

db = MySQLDatabase(host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")), user=os.environ.get("DB_USER"), passwd=os.environ.get("DB_PASS"), database=os.environ.get("DB_DATABASE"))
db.connect()
db.create_tables([User, BeerScore, UserGroup])
db.close()
