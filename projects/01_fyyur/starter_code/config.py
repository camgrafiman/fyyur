import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

print("///////////////////////configuración cargada!!")

# DONE IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://Alejandro:ghostrider87@localhost:5433/fyyur_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
