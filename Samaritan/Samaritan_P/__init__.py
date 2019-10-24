import os
import pyrebase
from flask import Flask

config = {
  'Get this from firebase'

}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Generate your random number here'
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()



from Samaritan_P import routes
