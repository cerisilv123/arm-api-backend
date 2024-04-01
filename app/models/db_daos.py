import pytz
import uuid
from datetime import datetime

from app import db

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    count = db.Column(db.Integer, nullable=False, default=1) 

    # Relationships
    itemsets = db.relationship('Itemset', backref='result', lazy=True)
    rules = db.relationship('Rule', backref='result', lazy=True)

class Itemset(db.Model):
    __tablename__ = 'itemset'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    items = db.Column(db.String(1000), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    # Relationships
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)

class Rule(db.Model):
    __tablename__ = 'rule'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    confidence = db.Column(db.Float, nullable=False)
    conviction = db.Column(db.Float, nullable=False)
    lift = db.Column(db.Float, nullable=False)
    support = db.Column(db.Float, nullable=False)
    rule = db.Column(db.String(1000), nullable=False)

    # Relationships
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)

    lhs = db.relationship('LHS', backref='rule', lazy=True)
    rhs = db.relationship('RHS', backref='rule', lazy=True)

class LHS(db.Model):
    __tablename__ = 'lhs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item = db.Column(db.String(200), nullable=False)

    # Relationships
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)

class RHS(db.Model):
    __tablename__ = 'rhs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item = db.Column(db.String(200), nullable=False)

    # Relationships
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)





