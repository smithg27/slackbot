import peewee
from peewee import *
import settings
import os

db = MySQLDatabase(host=os.environ.get("DB_HOST"), port=int(os.environ.get("DB_PORT")), user=os.environ.get("DB_USER"), passwd=os.environ.get("DB_PASS"), database=os.environ.get("DB_DATABASE"))

class BaseModel(peewee.Model):
    class Meta:
        database = db

class BeerScore(BaseModel):
    slackId = peewee.CharField()
    beers_to_give = peewee.IntegerField()
    beers_given = peewee.IntegerField()

    def give_beer(self, user2):
        if self.beers_to_give > 0:
            self.remove_beer()
            user2.get_beer()
            return True
        else:
            return False

    def remove_beer(self):
        self.beers_to_give -= 1
        self.save()

    def get_beer(self):
        self.beers_given += 1
        self.save()

    def reset_beer(self):
        self.beers_to_give = 5

    def get_score(self):
        return self.beers_given

class User(BaseModel):
    displayName = peewee.CharField()
    slackid = peewee.CharField()

class UserGroup(BaseModel):
    groupName = peewee.CharField()
    permissionsLevel = peewee.IntegerField()
