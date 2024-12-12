import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Photos(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.String(4096), default = '')
    # user_id = db.Column(db.Integer, backref=db.backref('Users'))
    date = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def login():
    return "na dzis koniec"


@app.route('/main_page')
def main_page():
    pass

if __name__ == '__main__':
    app.run()