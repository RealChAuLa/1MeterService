import os
import firebase_admin
from firebase_admin import credentials, db
from app.config import FIREBASE_URL

# Path to your Firebase service account file
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "path/to/serviceAccountKey.json")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_app = firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_URL
})


# Helper class to wrap Firebase Realtime Database operations with chaining
class DatabaseReference:
    def __init__(self, ref=None):
        self.ref = ref if ref else db.reference()

    def child(self, path):
        return DatabaseReference(self.ref.child(path))

    def get(self):
        return self.ref.get()

    def set(self, data):
        self.ref.set(data)

    def update(self, data):
        self.ref.update(data)


# Database reference wrapper
database = DatabaseReference()


# Function to check if a user exists
def user_exists(username):
    user_data = database.child('user_details').child(username).get()
    return user_data is not None


# Function to create a user
def create_user_in_db(username, user_data):
    database.child('user_details').child(username).set(user_data)


# Function to get user
def get_user(username):
    return database.child('user_details').child(username).get()

#Function to get product_id
def get_product_id(username):
    return database.child('user_details').child(username).child('product_id').get()