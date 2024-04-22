import pytz
import uuid
from datetime import datetime

from app import db

class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    count = db.Column(db.Integer, nullable=False, default=1) 
    algorithm = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.String(100), default=lambda: datetime.now(pytz.timezone('Europe/London')).strftime("%d/%m/%Y, %H:%M:%S"), nullable=False)

    # Relationships
    itemsets = db.relationship('Itemset', backref='result', lazy=True, cascade="all, delete-orphan")
    rules = db.relationship('Rule', backref='result', lazy=True, cascade="all, delete-orphan")

    def to_dict(self): 
        # Convert each LHS object to a dictionary and add it to the lhs list
        itemsets_list = [item.to_dict() for item in self.itemsets]
        
        # Convert each RHS object to a dictionary and add it to the rhs list
        rules_list = [item.to_dict() for item in self.rules]

        return {
            'id': self.id, 
            'count': self.count, 
            'algorithm': self.algorithm, 
            'date_added': self.date_added,
            'itemsets': itemsets_list, 
            'rules': rules_list,
        }

class Itemset(db.Model):
    __tablename__ = 'itemset'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    items = db.Column(db.String(1000), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    # Relationships
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 
            'items': self.items, 
            'count': self.count, 
        }

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

    lhs = db.relationship('LHS', backref='rule', lazy=True, cascade="all, delete-orphan")
    rhs = db.relationship('RHS', backref='rule', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        # Convert each LHS object to a dictionary and add it to the lhs list
        lhs_list = [item.to_dict() for item in self.lhs]
        
        # Convert each RHS object to a dictionary and add it to the rhs list
        rhs_list = [item.to_dict() for item in self.rhs]

        return {
            'id': self.id, 
            'confidence': self.confidence, 
            'conviction': self.conviction, 
            'lift': self.lift, 
            'support': self.support, 
            'rule': self.rule, 
            'lhs': lhs_list, 
            'rhs': rhs_list
        }

class LHS(db.Model):
    __tablename__ = 'lhs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item = db.Column(db.String(200), nullable=False)

    # Relationships
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 
            'item': self.item,
        }

class RHS(db.Model):
    __tablename__ = 'rhs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item = db.Column(db.String(200), nullable=False)

    # Relationships
    rule_id = db.Column(db.Integer, db.ForeignKey('rule.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id, 
            'item': self.item,
        }





