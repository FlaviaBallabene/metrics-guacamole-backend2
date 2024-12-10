from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
    campaigns = db.relationship('Campaign', back_populates='user')
    role = db.relationship('Role', back_populates='users')


    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,           
            "email": self.email,
            "campaigns": [campaign.serialize() for campaign in self.campaigns]
            # do not serialize the password, its a security breach
        }

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return '<Role %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "users": [user.serialize() for user in self.users]
        }


location_campaign = db.Table(
    "location_campaign",
    db.Column("location_id", db.Integer, db.ForeignKey("location.id"), primary_key=True),
    db.Column("campaign_id", db.Integer, db.ForeignKey("campaign.id"), primary_key=True)
)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platform.id'), nullable=False)

    user = db.relationship('User', back_populates='campaigns')
    project = db.relationship('Project', back_populates='campaigns')
    platform = db.relationship('Platform', back_populates='campaigns')
    weekly_data = db.relationship('WeeklyData', back_populates='campaign') #
    locations = db.relationship('Location', secondary=location_campaign, back_populates='campaigns')

    def __repr__(self):
        return '<Campaign %r>' % self.name
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "budget": self.budget,
            "notes": self.notes,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "platform_id": self.platform_id, 
            "weekly_data": [week.serialize() for week in self.weekly_data],
            "locations":[location.name for location in self.locations]
        }

class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    campaigns = db.relationship('Campaign', secondary=location_campaign, back_populates='locations')

    def __repr__(self):
        return '<Location %r>' % self.name


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    campaigns = db.relationship('Campaign', back_populates='project')

    def __repr__(self):
        return '<Project %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "campaigns": [campaign.serialize() for campaign in self.campaigns]
        }

class Platform(db.Model):
    __tablename__ = 'platform'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    campaigns = db.relationship('Campaign', back_populates='platform')

    def __repr__(self):
        return '<Platform %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "campaigns": [campaign.serialize() for campaign in self.campaigns]
        }
    

class WeeklyData(db.Model):
    __tablename__ = 'weekly_data'
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    spending = db.Column(db.Float, nullable=False)
    impressions = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, nullable=False)
    conversions = db.Column(db.Integer, nullable=False)

    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    campaign = db.relationship('Campaign', back_populates='weekly_data') #

    def serialize(self):
        return {
            "id": self.id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "spending": self.spending,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "conversions": self.conversions,
            "campaign_id":self.campaign_id
        }


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }