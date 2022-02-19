from sqlalchemy import update
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C://Users//331704//PycharmProjects//BlogItmo//database.db'
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.utcnow())
    likes = db.Column(db.Integer(), default=0)
    author = db.Column(db.Text(), nullable=False)


def get_db_connection():
    pass


def get_post(post_id):
    return Post.query.get(post_id)


def get_all_posts():
    return Post.query.all()


def delete_post(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()


def add_post(title, content, author):
    new_post = Post(title=title, content=content, author=author)
    db.session.add(new_post)
    db.session.commit()


def update_post(title, content, id):
    db.session.execute(update(Post)
                       .where(Post.id == id)
                       .values(title=title, content=content))
    db.session.commit()


add_post("123", "456", "123")
