import configparser
import os
from pyfiglet import Figlet
from tools import hashing
from loguru import logger

'''
brry CDN
tools/setup.py
'''

version = "0.2.0"
custom_fig = Figlet(font="slant")
config = configparser.ConfigParser()


def start():
    print(custom_fig.renderText("brry CDN"))
    print("Version: {0} \nLicense: General Copyright \nAuthor: berrysauce\n".format(version))
    try:
        with open("data/config.ini", "r") as f:
            f.read()
    except IOError:
        logger.warning("Starting setup - no config found")
        try:
            os.mkdir("data")
            logger.info("Created 'data' folder")
        except:
            logger.error("The 'data' folder already exists. Please delete it and try again.")
            logger.warning("Canceling setup and stopping app")
            quit()
        try:
            os.mkdir("data/images")
            logger.info("Created 'data/images' folder")
        except:
            logger.error("The 'data/images' folder already exists. Please delete it and try again.")
            logger.warning("Canceling setup and stopping app")
            quit()
        
        print(50 * "-")
        print("Starting setup - all values (except the Password) \ncan be changed in data/config.ini.")

        print(" \n[1/4] What's your host? Press enter to use the default (localhost).")
        host = input(">>> ")
        if not host:
            host = "127.0.0.1"

        print(" \n[2/4] What's your port? Press enter to use the default (80).")
        port = input(">>> ")
        if not port:
            port = "80"

        print(
            " \n[3/4] What's your username? Press enter to use the default (Admin).")
        redirect = input(">>> ")
        if not redirect:
            username = "Admin"

        print(" \n[4/4] Please enter your Password for accessing the API. Keep this secret!")
        password = input(">>> ")

        print(50 * "-")
        logger.info("Creating config")

        hashedpassword = hashing.hashpw(password)

        config["SERVER"] = {"host": host,
                            "port": port,
                            "username": username,
                            "password": hashedpassword}
        with open("data/config.ini", "w") as configfile:
            config.write(configfile)
        logger.info("Created config")