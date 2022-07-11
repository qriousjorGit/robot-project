from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import pprint as p


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
import os

app = Flask(__name__)


# Create DB using SQLalchemy
class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///robotbase2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.String(100), unique=False, nullable=True)
    robot_name = db.Column(db.String(100), unique=False, nullable=True)
    robot_deactivated = db.Column(db.String(100), unique=False, nullable=True)
    robot_photo = db.Column(db.String(100), unique=False, nullable=True)
    robot_title = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<Botlist %r>' % self.robot_name


# Create new .db if not present
if not os.path.isfile('sqlite:///robotbase2.db'):
    db.create_all()



#SLACK API code below

""" We need to pass the 'Bot User OAuth Token' """
slack_token = os.environ.get("SLACK_BOT_TOKEN")
# Creating an instance of the Webclient class
client = WebClient(token=slack_token)


# Convert unixtimestamp to "human date"
def convert_unixtime (ts: int):
    return (datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y'))
    # with time (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))


try:
    # Get list of all users
    user_list = []
    users = client.users_list(limit=500)
    # print(users)
    for item in users.get("members"):
        user_list.append(item)

    # Slack API returns this in pages, need to cycle through to get all results
    # https://api.slack.com/docs/pagination
    next_cursor = users.get("response_metadata").get("next_cursor")

    while len(user_list) < 5000:
        users = client.users_list(limit=500, cursor=next_cursor)
        # print(next_cursor)
        for item in users.get("members"):
            user_list.append(item)

        print(len(user_list))
        next_cursor = users.get("response_metadata").get("next_cursor")

# Create the DB for all robots that left starting January 2022 from the full "user_list"
    bye_list = []
    for entries in user_list:
        isJan9 = str(entries.get("updated")).startswith("16417")

        if entries.get("deleted") == True and isJan9 is False:
            unix_time = entries.get("updated")
            human_time = convert_unixtime(unix_time)
            #TODO this will all need to go into a database for permanent storage and then used for the website
            # print(entries.get("id"), entries.get("tz"), entries.get("profile").get("real_name"), human_time, unix_time,
            #       entries.get("profile").get("title"))
            # bye_list.append(entries)

            # check if entry is already in the DB
            exists = db.session.query(Robot.id).filter_by(robot_id=entries.get('id')).first() is not None
            # print(exists)
            if exists is False:
                new_bot = Robot(robot_id=entries.get('id'), robot_name=entries.get('profile').get('real_name'), robot_deactivated=human_time,
                            robot_photo=entries.get('profile').get('image_192'), robot_title=entries.get("profile").get("title"))

                db.session.add(new_bot)
                db.session.commit()

    # print(f"Bye length= {len(bye_list)}")

except SlackApiError as e:
    assert e.response["error"]
    print("Got an error")

olga = "UL9UG909Z"
guy = "U02SDPLDH"
elena = "U0296SQ5EQ4"
colin = "U0CJM5WGL"
darren = "UMQS1NMMX"
oleg = "ULL9RN5QB"
mike = "UK0R1SBDX"
jeremy = "U02SDPLDH"

# TODO: using the "updated" attribute is not always accurate,
#  Many profiles appear to have been updated on ~Jan 9 2022 despite being deactivated much earlier
#  All start with 16417 i.e. Darren/Jeremy/Mike/oleg
#  More recent updates like Colin/Elena are accurate (May12/April 29)
#  Also, "team_id" doesn't seem to mean anything

def when_updated(user):
    data = lookup(user)
    unix_update_time = data['user']['updated']
    print(f"Last update: {unix_update_time}")
    #TODO - replace below code with a function.  Definitely CANNOT make a request for each of these
    # r = requests.get(url=f"https://showcase.api.linx.twenty57.net/UnixTime/fromunix?timestamp={unix_update_time}")
    # print(r.text)
    return(convert_unixtime(unix_update_time))


##Lookup user infor by "id" for example U709M2WDP
## Returns a Slack object - documentation here - https://slack.dev/python-slack-sdk/api-docs/slack_sdk/web/slack_response.html
def lookup(id):
    """Returns a dictionary with the users information"""
    try:
        response = client.users_info(user=id)
        return response.data
    except SlackApiError as e:
        assert e.response["error"]
        print("Got an error")


# d = lookup(jeremy)
#
# print(d.get("user").get("id"),
#       d.get("user").get("profile").get("real_name"),
#       d.get("user").get("profile").get("image_72"),
#       d.get("user").get("updated")
#       )
# print(when_updated(jeremy))



# Check for last activity ("last_activity" deprecated?? https://api.slack.com/methods/users.getPresence)
# Might only work if "user" is still active.  Documentation isn't very clear
def last_activity(id):
    response = client.users_getPresence(user=id)
    print(response.data)


