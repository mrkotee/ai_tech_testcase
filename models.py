import os
from flask_sqlalchemy import SQLAlchemy
from app import app


db_path = os.path.join(os.getcwd(), 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

rubrics = db.Table('rubrics',
                   db.Column('rubric_id', db.Integer, db.ForeignKey('rubric.id'), primary_key=True),
                   db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True)
                   )


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    rubrics = db.relationship('Rubric', secondary=rubrics, lazy='subquery',
                           backref=db.backref('documents', lazy=True))


class Rubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


if not os.path.exists(db_path):  # create sqlite db file
    db.create_all()
