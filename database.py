import os
from dotenv import load_dotenv

from peewee import *


load_dotenv()

USERNAME = os.getenv('USERDB')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')

database = MySQLDatabase(DATABASE, user=USERNAME, password=PASSWORD, host=HOST, port=int(PORT))
