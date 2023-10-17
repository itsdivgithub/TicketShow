from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from werkzeug.security import generate_password_hash, check_password_hash


import datetime
from datetime import datetime
from pytz import timezone

#  -------------------------------------

db = SQLAlchemy()

#  -------------------------------------


# User table
class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean())
    bookings = db.relationship('Bookings', backref='User', lazy=True)

    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"


# Role table
class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description=db.Column(db.String(20), unique=True, nullable=False)
    
    def __repr__(self):
        return f"Role(id={self.id}, name='{self.name}')"

# Venue table
class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    location= db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='Venue', lazy=True)

    def __repr__(self):
        return f"Venue(id={self.id}, name='{self.name}', place='{self.place}', capacity={self.capacity}, )"
    
# Show table
class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(100), nullable=False)
    timings = db.Column(db.String(100), nullable=False) 
    ticket_price = db.Column(db.Integer, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    bookings = db.relationship('Bookings', backref='Show', lazy= 'subquery')

    def __repr__(self):
        return f"Show(id={self.id}, name='{self.name}', rating={self.rating}, timings='{self.timings}',tags='{self.tags}', ticket_price={self.ticket_price})"
    
    @property
    def total_seats_booked(self):
        return sum(booking.seats_booked for booking in self.bookings)
    
    

# Bookings table
class Bookings(db.Model):
    __tablename__ = 'Bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('Show.id'), nullable=False)
    seats_booked = db.Column(db.Integer, nullable=False)
    booked_cost= db.Column(db.Integer, nullable=False)
    booked_time= db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    
    def __repr__(self):
        return f"Bookings(id={self.id}, user_id={self.user_id}, show_id={self.show_id}, seats_booked={self.seats_booked})"