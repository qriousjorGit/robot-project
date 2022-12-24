from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
import pprint as p
import time
import random


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
import os

from linkedin import search

app = Flask(__name__)


# Create DB using SQLalchemy
class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rb3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Robot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    robot_id = db.Column(db.String(100), unique=False, nullable=True)
    robot_name = db.Column(db.String(100), unique=False, nullable=True)
    robot_deactivated = db.Column(db.String(100), unique=False, nullable=True)
    robot_photo = db.Column(db.String(100), unique=False, nullable=True)
    robot_title = db.Column(db.String(100), unique=False, nullable=True)
    robot_link = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
        return '<Botlist %r>' % self.robot_name


all_bots = db.session.query(Robot).all()
# print(all_bots)
print(len(all_bots))

bot_id = 825

# print(search('steph kim'))

for bot in all_bots:
    try:
        bot_to_update = Robot.query.get(bot_id)
        # print(bot_to_update.id, bot_to_update.robot_name, bot_to_update.robot_link)
        bot_to_update.robot_link = search(bot_to_update.robot_name)
        print(bot_to_update.id, bot_to_update.robot_name, bot_to_update.robot_link)
        db.session.commit()
        bot_id += 1
        # time.sleep(random.randint(1, 7))
    except AttributeError:
        bot_id += 1
    except IndexError:
        bot_id +=1



#
#
# for bot in all_bots[:5]:
#     print(bot.robot_name, bot.id)
#     # print(search(bot.robot_name))
#     bot.robot_link = search(bot.robot_name)
#     print(bot.robot_link)
