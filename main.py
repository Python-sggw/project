import os
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_security import Security, UserMixin, RoleMixin, SQLAlchemyUserDatastore, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import random as rd
import pkg_resources

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'developerskie')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'jakas-sol')
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
UPLOAD_FOLDER = './static/photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Funkcja sprawdzająca rozszerzenie pliku

db = SQLAlchemy(app)

roles_user = db.Table(
    'roles_users',
    db.Column('user_id', db.ForeignKey('user.user_id')),
    db.Column('role_id', db.ForeignKey('role.id')),
)

class Photos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.String(4096), default = '')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.DateTime, default=datetime.now)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(128))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    confirmed_at = db.Column(db.DateTime)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)  
    roles = db.relationship('Role', secondary=roles_user, backref=db.backref('users'))
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if not self.fs_uniquifier:
            import uuid
            self.fs_uniquifier = str(uuid.uuid4())


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

def add():
    photo1 = Photos( 
        name = "1.jpg",
        likes = 10,
        comments = "Fajny Samolot\nFajny\nNiezly!",
        user_id = "testowy1"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        name = "2.jpg",
        likes = 1,
        comments = "Fajny Samolot!\nFajny!\nNiezly!",
        user_id = "testowy2"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        name = "3.jpg",
        likes = 5,
        comments = "Fajny Samolot!!!\nFajny\nNiezly!",
        user_id = "testowy3"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        name = "4.jpg",
        likes = 20,
        comments = "Fajny Samolot\nFajny!!!!\nNiezly!",
        user_id = "testowy4"
    )
    db.session.add(photo1)
    db.session.commit()
    photo1 = Photos( 
        name = "5.jpg",
        likes = 30,
        comments = "Fajny\nFajny\nNiezly!",
        user_id = "testowy5"
    )
    db.session.add(photo1)
    db.session.commit()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/like', methods=['POST'])
@login_required
def like_photo():
    data = request.json
    photo_id = data.get('id')
    if photo_id:
        photo = Photos.query.filter_by(id=photo_id).first()  
        if photo:
            photo.likes += 1 
            db.session.commit()  
            return {"success": True, "likes": photo.likes}, 200 
        else:
            return {"success": False, "message": "Photo not found"}, 404 
    return {"success": False, "message": "No photo ID provided"}, 400  

@app.route('/comment', methods=['POST'])
@login_required
def add_comment():
    data = request.json
    photo_id = data.get('id')
    new_comment = data.get('comment')
    if not photo_id or not new_comment:
        return {"success": False, "message": "Invalid data"}, 400
    photo = Photos.query.filter_by(id=photo_id).first()
    if not photo:
        return {"success": False, "message": "Photo not found"}, 404
    photo.comments += f"\n{new_comment}" if photo.comments else new_comment
    db.session.commit()
    return {"success": True, "comment": new_comment}, 200


@app.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            
            new_photo = Photos(
                name=file.filename,
                likes=0,
                comments="",
                user_id = current_user.get_id()
            )
            db.session.add(new_photo)
            db.session.commit()

            flash('Photo added successfully!')
            return redirect(url_for('main_page'))
    return render_template('new_post.html')



@app.route('/')
@login_required
def main_page():
    photos = Photos.query.all()
    rd.shuffle(photos)
    photos = photos[:5]
    posts = [
        {
            "id": photo.id,
            "username": f"{photo.user_id}",
            "image": f"./photos/{photo.name}",
            "likes": photo.likes,
            "comments": photo.comments.split('\n')
        } for photo in photos
    ]

    print(current_user.get_id())

    return render_template('main_page.html', posts=posts)



if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
    #     add()
    app.run()