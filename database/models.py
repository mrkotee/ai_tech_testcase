import os
from flask_sqlalchemy import SQLAlchemy
from flask_app.app import app
from settings import db_path


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

    def delete(self):
        for rubric in self.rubrics:
            if len(rubric.documents) == 1:
                db.session.delete(rubric)
        db.session.delete(self)
        db.session.commit()


class Rubric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


