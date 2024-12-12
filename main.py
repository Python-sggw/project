import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)

class Photos(db.Model):
    photo_id = db.Column(db.String(255), primary_key=True)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.String(4096), default = '')
    # user_id = db.Column(db.Integer, backref=db.backref('Users'))
    date = db.Column(db.DateTime, default=datetime.now)

def add():
    photo1 = Photos( 
        photo_id = "1.jpg",
        likes = 10,
        comments = "Fajny Samolot\nFajny\nNiezly!"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        photo_id = "2.jpg",
        likes = 1,
        comments = "Fajny Samolot!\nFajny!\nNiezly!"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        photo_id = "3.jpg",
        likes = 5,
        comments = "Fajny Samolot!!!\nFajny\nNiezly!"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        photo_id = "4.jpg",
        likes = 20,
        comments = "Fajny Samolot\nFajny!!!!\nNiezly!"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        photo_id = "5.jpg",
        likes = 30,
        comments = "Fajny\nFajny\nNiezly!"
    )
    db.session.add(photo1)
    db.session.commit()

@app.route('/')
def main_page():
    #add()
    photos = Photos.query.all()
    posts = [
        {
            "username": "Unknown",
            "image": f"./photos/{photo.photo_id}",
            "likes": photo.likes,
            "comments": photo.comments.split('\n')
        } for photo in photos
    ]
    return render_template('main_page.html', posts=posts)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    app.run()