from slackclient import SlackClient
import time
import json
import os
import re
from database.models import *



slack_token = os.environ.get("SLACK_TOKEN")
sc = SlackClient(slack_token)
starterbot_id = None
db.connect()



if sc.rtm_connect():
    starterbot_id = sc.api_call("auth.test")["user_id"]
    botid_string = "<@" + starterbot_id.lower() + ">"
    membersList = sc.api_call('users.list')
    for member in membersList['members']:
        User, created = User.get_or_create(
            displayName=member['profile']['display_name'],
            slackid=member['id']
        )
        beerScore, created = BeerScore.get_or_create(
            slackId=member['id'],
            beers_to_give=25,
            beers_given=0
        )

    while True:
        message = sc.rtm_read()
        if len(message) > 0:
            print(message)
            textLower = message[0].get('text', 'Empty').lower()
            if botid_string in textLower:
                MatchString = re.findall(r"(?<=<@)\S{9}(?=>)", textLower)
                if message[0].get('user'):
                    if message[0].get('user').lower() != botid_string.lower():
                        if MatchString[0] == starterbot_id.lower():
                            if "help" in textLower:
                                data = message[0].get('text').lower().split()
                                if data[-1] == "help":
                                    string = "What would you like help with? Use @kudobot help <command> to get more help \n"
                                    string += ">>>1. beerscore"
                                if data[-1] == "beerscore":
                                    string = "Beerscore is a kudo tracker where you can give beer to other users. To find out more type @kudobot help beerscore <command> \n"
                                    string += ">>>1. :beer: \n 2. myscore \n 3. leaderboard"
                                if data[-2] == "beerscore":
                                    if data[-1] == ":beer:":
                                        string = "Give beer to other users by typing `@kudobot :beer: @user_to_get_beer`"
                                    elif data[-1] == "myscore":
                                        string = "To see how many beers you have type `@kudobot beerscore myscore`"
                                    elif data[-1] == "leaderboard":
                                        string = "To see who has the most beer type `@kudobot beerscore leaderboard`"
                                if string:
                                    sc.api_call(
                                        "chat.postMessage",
                                        channel=message[0].get('channel'),
                                        text=string
                                    )
                            elif "beerscore myscore" in message[0].get('text').lower():
                                slackId = message[0].get('user')
                                User = BeerScore.get(BeerScore.slackId == message[0].get('user'))
                                string = User.beers_given
                                sc.api_call(
                                    "chat.postMessage",
                                    channel=message[0].get('channel'),
                                    text=string
                                )

                            elif "beerscore leaderboard" in message[0].get('text').lower():
                                string = ">>> "
                                rank = 1
                                for p in BeerScore.select().order_by(BeerScore.beers_given.desc()).limit(3):
                                    string += str(rank) + ". <@" + p.slackId + '> Beers received: ' + str(
                                        p.beers_given) + "\n"
                                    rank += 1
                                sc.api_call(
                                    "chat.postMessage",
                                    channel=message[0].get('channel'),
                                    text=string
                                )
                            elif ":beer:" in message[0].get('text').lower() and MatchString[1]:
                                beerCount = re.findall(r":beer:", textLower)
                                beerCount = len(beerCount)
                                i = 1
                                while i <= beerCount:
                                    if MatchString[1] != message[0].get('user').lower():
                                        beerGiver, created = BeerScore.get_or_create(
                                            slackId=message[0].get('user')
                                        )

                                        beerReciever, created = BeerScore.get_or_create(
                                            slackId=MatchString[1]
                                        )
                                        if beerGiver.give_beer(beerReciever):
                                            string = "> :beer: given to <@" + MatchString[1].upper() + "> by <@" + message[0].get(
                                                'user') + ">"
                                        else:
                                            string = "<@" + message[0].get('user') + "> You are out of beers to give."
                                        i += 1
                                        sc.api_call(
                                            "chat.postMessage",
                                            channel=message[0].get('channel'),
                                            text=string
                                        )
                                        # if i > 5:
                                        #     break
                            elif "roster" in message[0].get('text').lower():
                                data = message[0].get('text').lower().split()
                                team = data[-1]
                                



        time.sleep(1)
else:
    print("Connection Failed")
