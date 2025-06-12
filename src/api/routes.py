"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException, send_email
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode
import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


api = Blueprint('api', __name__)

# manejo de hash de contraseña


def set_password(password, salt):
    return generate_password_hash(f"{password}{salt}")


def check_password(pass_hash, password, salt):
    """
        hashpasswor === 12345678salt 
    """

    return check_password_hash(pass_hash, f"{password}{salt}")

# final manejo de hash de contraseña


expires_in_minutes = 10
expires_delta = timedelta(minutes=expires_in_minutes)


# Allow CORS requests to this API
CORS(api)


@api.route('/healt-check', methods=['GET'])
def handle_hello():

    return jsonify("ok"), 200


@api.route("/register", methods=["POST"])
def add_user():
    data = request.json  # recimos dados del body
    email = data.get("email", None)
    lastname = data.get("lastname", None)
    password = data.get("password", None)
    salt = b64encode(os.urandom(32)).decode("utf-8")

    if email is None or password is None or lastname is None:
        return jsonify("You a need an password, lastname and a email"), 400

    user = User()
    user.email = email
    user.lastname = lastname
    user.password = set_password(password, salt)
    user.salt = salt

    db.session.add(user)

    try:
        db.session.commit()
        return jsonify("User created"), 201
    except Exception as error:
        db.session.rollback()
        return jsonify(f"Error:  {error.args}"), 500


@api.route("/login", methods=["POST"])
def handle_login():
    data = request.json  # passwod y email

    email = data.get("email", None)
    password = data.get("password", None)

    if email is None or password is None:
        return jsonify("You a need an password and a email"), 400

    else:
        # cosulto si ese email esta registrado, la db me responde user o None
        user = User.query.filter_by(
            email=email).one_or_none()  # None, 1, 2(error)
        if user is None:
            return jsonify("Bad email"), 400
        else:
            if check_password(user.password, password, user.salt):
                # debems generar el token
                token = create_access_token(identity=str(user.id))

                return jsonify({
                    "token": token
                }), 200
            else:
                return jsonify("Bad password"), 400


@api.route("/user", methods=["GET"])
@jwt_required()
def get_all_users():
    users = User.query.all()

    return jsonify(list(map(lambda item: item.serialize(), users))), 200


@api.route("/me", methods=["GET"])
@jwt_required()  # proceso solo consultas con token
def get_one_user():
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user is None:
        return jsonify("User not found"), 404

    return jsonify(user.serialize())


@api.route("/reset-password", methods=["POST"])
def reset_password():
    # necesitamos el correo para evviar el link de recuperación
    body = request.json  # dvasquez@4geeksacademy.com

    user = User.query.filter_by(email=body).one_or_none()

    if user is None:
        return jsonify("user not found"), 404

    access_token = create_access_token(
        identity=body, expires_delta=expires_delta)

    message = f"""
        <a href="https://humble-guide-ppgwrqgxxvjfr4w9-3000.app.github.dev/update-pass?token?{access_token}">recuperaar contraseña</a>
    """

    data = {
        "subject": "Recuperación de contraseña",
        "to": body,
        "message": message
    }

    sended_email = send_email(
        data.get("subject"), data.get("to"), data.get("message"))

    if sended_email:
        return jsonify("Message dended"), 200
    else:
        return jsonify("Error"), 200


@api.route("/update-password", methods=["PUT"])
@jwt_required()
def update_password():
    user_token_email = get_jwt_identity()
    password = request.json

    user = User.query.filter_by(email=user_token_email).first()

    if user is not None:
        salt = b64encode(os.urandom(32)).decode("utf-8")
        password = set_password(password, salt)

        user.salt = salt
        user.password = password

        try:
            db.session.commit()
            return jsonify("password changed successfuly"), 201
        except Exception as error:
            db.session.rollback()
            return jsonify("Error"), 500

    print(user.serialize)
