import hashlib

import os
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime

from peewee import *

load_dotenv()

USERNAME = os.getenv('USERDB')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORTDB')
DATABASE = os.getenv('DATABASE')

database = MySQLDatabase(DATABASE, user=USERNAME, password=PASSWORD, host=HOST, port=int(PORT))


class Nivel(Model):
    nombre = CharField(max_length=15)
    tipo = IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        database = database
        table_name = 'niveles'


class Marca(Model):
    nombre = CharField(max_length=30)

    def __str__(self):
        return self.nombre

    class Meta:
        database = database
        table_name = 'marcas'


class Usuario(Model):
    nivel = ForeignKeyField(Nivel, backref='nivel')
    username = CharField(max_length=20, unique=True)
    password = CharField(max_length=50)
    fecha_creacion = DateTimeField(default=datetime.now)
    nombre_completo = CharField(max_length=100)
    fecha_nacimiento = DateField()
    email = CharField(max_length=50)
    telefono = CharField(max_length=15)
    direccion = TextField()


    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = 'usuarios'

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()

        h.update(password.encode('utf-8'))
        return h.hexdigest()

class Producto(Model):
    marca = ForeignKeyField(Marca, backref='marca')
    sku = CharField(max_length=20, unique=True)
    nombre = CharField(max_length=150)
    precio = FloatField()
    fecha_alta = DateTimeField(default=datetime.now)
    estatus = BooleanField()

    def __str__(self):
        return self.nombre

    class Meta:
        database = database
        table_name = 'productos'

class SeguimientoUsuario(Model):
    usuario = ForeignKeyField(Usuario, backref='seguimiento')
    producto = ForeignKeyField(Producto, backref='seguimiento')
    fecha_visita = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.fecha_visita} | {self.usuario} | {self.producto}'

    class Meta:
        database = database
        table_name = 'usuarios_seguimientos'