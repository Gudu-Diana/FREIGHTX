from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

from config import db, bcrypt

# Models go here!
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_rules = ('-password', '-passengers.user')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    passengers = db.relationship('Passenger', back_populates='user')
    ships = association_proxy('passengers', 'ship')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    def __repr__(self):
      return f'<User {self.name}>'

class Passenger(db.Model):
    __tablename__ = "passengers"
    serialize_rules = ('-user.passengers', '-ship.passengers')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticket_number = db.Column(db.String(10), unique=True, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=True)
    ship = db.relationship('Ship', back_populates='passengers')
    user = db.relationship('User', back_populates='passengers')

    def __repr__(self):
      return f'<Passenger {self.ticket_number}>'

class Ship(db.Model):
    __tablename__ ="ships"
    serialize_rules = ('-contractor.ships', '-port.ships', '-passengers.ship')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    capacity_weight = db.Column(db.Float, nullable=False)
    current_weight = db.Column(db.Float, default=0.0)
    total_tickets = db.Column(db.Integer, nullable=False)
    available_tickets = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String)
    port_id = db.Column(db.Integer, db.ForeignKey('ports.id'), nullable=False)
    contractor_id = db.Column(db.Integer,db.ForeignKey('contractors.id'), nullable= False )
    passengers = db.relationship('Passenger', back_populates='ship')
    contractor = db.relationship('Contractor', back_populates='ships')
    port = db.relationship('Port', back_populates='ships')
    
    def __repr__(self):
        return f'<Ship {self.name}>'
    
class Port(db.Model, SerializerMixin):
  __tablename__ = "ports"   
  serialize_rules = ('-ships.port') 
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  location = db.Column(db.String, nullable=False)
  image_url = db.Column(db.String)
  ships = db.relationship('Ship', back_populates='port')

  def __repr__(self):
      return f'<Port {self.name}>'
  
class Contractor(db.Model, SerializerMixin):
  __tablename__ = "contractors"
  serialize_rules = ('-ships.contractor',)
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  specialization = db.Column(db.String)
  contact_info = db.Column(db.String)
  ships = db.relationship('Ship', back_populates='contractor')

  def __repr__(self):
      return f'<Contractor {self.name}>'

  
class UserShipAssociation(db.Model, SerializerMixin):
    __tablename__ = 'user_ship_association'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=False)
