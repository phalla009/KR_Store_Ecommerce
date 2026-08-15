import os
from flask import Flask

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Telegram & Currency Settings
BOT_TOKEN = os.environ.get(
    'BOT_TOKEN', '8282363808:AAGT0lAZyrs8Q5gTUDY2hgpfBDc_4KfepIk'
)
CHAT_ID = os.environ.get('CHAT_ID', '@khchelrien2024')
USD_TO_KHR = 4100

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'hphalla@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get(
    'MAIL_PASSWORD', 'iflq jnct ngwy ucqg'
)
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get(
    'MAIL_DEFAULT_SENDER', 'hphalla3@gmail.com'
)