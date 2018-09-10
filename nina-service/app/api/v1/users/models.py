# project/api/models.py


import datetime

import jwt
from flask import current_app
from flask_mail import Message

from app import db, bcrypt, mail
from helpers.functions.random import generate_random_string
from . import UploadMessenger
from flask import request

class Customer(db.Model):
    __tablename__ = "stripe_customer"
    id = db.Column(db.String(255), primary_key= True)
    user_id = db.Column(db.Integer, nullable= False)
    email = db.Column(db.String(255), primary_key= True)

class Plan(db.Model):
    __tablename__ = "stripe_plan"
    id = db.Column(db.String(255), primary_key= True)
    amount = db.Column(db.Integer, nullable= False)
    interval = db.Column(db.String(255), nullable= False)
    product_name = db.Column(db.String(255), nullable= False)
    currency = db.Column(db.String(255), nullable= False)

class Card(db.Model):
    __tablename__ = "stripe_card"
    id = db.Column(db.String(255), primary_key= True)
    type = db.Column(db.String(255), nullable= False)
    # expiration_month = db.Column(db.Integer, nullable= False)
    # expiration_year = db.Column(db.Integer, nullable= False)
    user_id = db.Column(db.Integer, nullable= False)


class Subscription(db.Model):
    __tablename__ = "stripe_subscription"
    id = db.Column(db.String(255), primary_key= True)
    stripe_customer_id = db.Column(db.String(255), nullable= True)
    stripe_plan_id = db.Column(db.String(255), nullable= True)
    amount = db.Column(db.Integer, nullable= True)
    expiration_date = db.Column(db.DateTime, nullable= False)
    # user_id = db.Column(db.Integer, nullable= False)


class ConfirmationCode(db.Model):
    __tablename__ = "confirmation_code"
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    user_id = db.Column(db.Integer, nullable= False)
    code = db.Column(db.String(255), nullable= False)
    activated = db.Column(db.Boolean, default= False)
    created_at = db.Column(db.DateTime, nullable= False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.code = generate_random_string()
        self.created_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key= True, autoincrement= True)
    name = db.Column(db.String(128), nullable= True)
    email = db.Column(db.String(128), unique= True, nullable= False)
    password = db.Column(db.String(255), nullable= False)
    admin = db.Column(db.Boolean, default= False, nullable= False)
    photo_url = db.Column(db.Text(), nullable= True)
    photo_name = db.Column(db.String(255), nullable= True)
    created_at = db.Column(db.DateTime, nullable= False)
    updated_at = db.Column(db.DateTime, nullable= False)
    pay_date = db.Column(db.DateTime, nullable= True)

    class Meta:
        updatable_fields = ('name', 'email', 'photo_url', 'photo_name')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def hash_password(self, password):
        return bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def _update_or_keep(self, field_name, form_field, output):
        if form_field.data:
            setattr(self, field_name, form_field.data)
            output[field_name] = form_field.data

    def update_password(self, password, old_password):
        print("PASSWORDS: ", password, old_password)
        if password and old_password:
            if not bcrypt.check_password_hash(self.password, old_password):
                raise Exception("Old password not match")
            if bcrypt.check_password_hash(self.password, password):
                raise Exception("New and old password are equal")
            self.password = self.hash_password(password)

    def delete_old_photo(self):
        UploadMessenger.set_headers(request)
        try:
            upload_response = UploadMessenger.send(
                params= self.photo_name,
                method= 'delete'
                )
        except Exception as e:
            pass

    def __init__(
            self, name, email, password):

        self.name = name
        self.email = email

        self.password = self.hash_password(password)

        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    @staticmethod
    def create_by_form(form):
        return User(
            name= form.name.data,
            email= form.email.data,
            password= form.password.data
            )

    def update_by_form(self, form):
        output = {}
        if form.photo_name.data:
            self.delete_old_photo()
        for field_name in self.Meta.updatable_fields:
            self._update_or_keep(field_name, getattr(form, field_name), output)
        self.update_password(form.password.data, form.old_password.data)
        self.updated_at = datetime.datetime.utcnow()
        return output


    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days= current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds= current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm= 'HS256'
            )
        except Exception as e:
            return e

    def send_conformation_code(self, to_email, code):
        try:
            msg = Message('Reset password', sender = 'testlviv9@gmail.com', recipients = [to_email, ])
            msg.body = "This is your confirmation url: http://35.229.107.184/forgot-password?param=%s \nDo not tell this code anyone" % code
            mail.send(msg)
            return True
        except Exception as e:
            raise e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token - :param auth_token: - :return: integer|string"""
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
