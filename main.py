from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from typing import Callable
import os

app = Flask(__name__)

#Create DB using SQalchemy

class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    Float: Callable

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///robotbase.db'
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
if not os.path.isfile('sqlite:///robotbase.db'):
    db.create_all()


#Add robots to the DB
new_bot = Robot(robot_id="uXASD", robot_name="bot 3 no dups", robot_deactivated="1423663634534512", robot_photo=" photo", robot_title="some title")
# db.session.add(new_bot)
# db.session.commit()

all_bots = db.session.query(Robot).all()
print(all_bots)
print(len(all_bots))

#check if entry is already in the DB
exists = db.session.query(Robot.id).filter_by(robot_id='uXASD').first() is not None
print(exists)



# if __name__ == "__main__":
#     app.run()
#
