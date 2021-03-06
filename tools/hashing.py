import hashlib
import binascii
import os
import configparser
from loguru import logger


'''
brry CDN
tools/hashing.py
Source: https://www.vitoshacademy.com/hashing-passwords-in-python/
'''

config = configparser.ConfigParser()

def hashpw(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwhash = binascii.hexlify(pwhash)
    logger.info("Hashed password")
    return (salt + pwhash).decode('ascii')


def verifypw(provided_password):
    config.read("data/config.ini")
    stored_password = config.get("SERVER", "password")
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwhash = binascii.hexlify(pwhash).decode('ascii')
    logger.info("Verified password")

    if pwhash == stored_password:
        return True
    else:
        return False