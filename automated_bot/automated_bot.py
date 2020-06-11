import os
import json
import requests
from faker import Faker
from random import randrange, choice
from dotenv import load_dotenv

class AutomatedBot:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None

    def signup(self, username, password, first_name=None, last_name=None, email=None):
        api_url = '{0}users/'.format(self.base_url)
        user_data = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }
        response = requests.post(api_url, headers=self.get_headers(), json=user_data)
        if response.status_code == 201:
            print("Successfully signed up a user!")
            print(json.loads(response.content.decode('utf-8')))
        else:
            print("Couldn't signup user with given data: ", user_data)

    def login(self, username, password):
        api_url = '{0}api/token/'.format(self.base_url)
        credentials = {'username': username, 'password': password}
        response = requests.post(api_url, headers=self.get_headers(), json=credentials)
        if response.status_code == 200:
            self.access_token = json.loads(response.content.decode('utf-8'))["access"]
            self.refresh_token = json.loads(response.content.decode('utf-8'))["refresh"]
            print("Login Successful!")
        else:
            print("Couldn't login!") 

    def refresh(self):
        if self.refresh_token is None:
            print("Missing Refresh Token! Please Login first!")
            return None
        api_url = '{0}api/token/refresh/'.format(self.base_url)
        body = {'refresh': self.refresh_token}
        response = requests.post(api_url, headers=self.get_headers(), json=body)
        if response.status_code == 200:
            self.access_token = json.loads(response.content.decode('utf-8'))["access"]
            print("Refreshed Access Token Successful!")
        else:
            print("Couldn't refresh Access Token! It may have expired. Please Login again!")

    def write_post(self, body):
        if not body:
            print("Cannot write empty post. Please provide a string value.")
            return None
        api_url = '{0}posts/'.format(self.base_url)
        body = {'body': body}
        response = requests.post(api_url, headers=self.get_headers(token=self.access_token), json=body)
        if response.status_code == 201:
            print("Successfully wrote a post!")
            post = json.loads(response.content.decode('utf-8'))
            print(post)
            return post
        else:
            print("Couldn't write a post")
            return None

    def like_post(self, post_id):
        if not post_id:
            print("Cannot like post without post_id. Please provide post_id.")
            return None
        api_url = '{0}posts/{1}/likes/'.format(self.base_url, post_id)
        response = requests.put(api_url, headers=self.get_headers(token=self.access_token))
        if response.status_code == 200:
            print("Successfully liked a post with ID={0}!".format(post_id))
            print(json.loads(response.content.decode('utf-8')))
        else:
            print("Couldn't like a post with ID={0}!".format(post_id))


    def get_headers(self, token=None):
        if token:
            return {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {0}'.format(token)
            }
        return {'Content-Type': 'application/json'}


load_dotenv()
fake = Faker()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER_NUM = os.getenv("USER_NUM")
MAX_POSTS_PER_USER = os.getenv("MAX_POSTS_PER_USER")
MAX_LIKES_PER_USER = os.getenv("MAX_LIKES_PER_USER")

if not HOST or not PORT or not USER_NUM or not MAX_LIKES_PER_USER or not MAX_LIKES_PER_USER:
    print("Please configure .env file properly and provide all necessary values.")
    exit()

bot = AutomatedBot("http://{0}:{1}/".format(HOST, PORT))

user_credentials = {}
post_ids = []

for i in range(int(USER_NUM)):
    
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name + last_name
    email = first_name + "." + last_name + "@email.com"
    password = "123TESTpassword"

    user_credentials[i] = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password
    }

    bot.signup(**user_credentials[i])

for i in range(int(USER_NUM)):
    username = user_credentials[i]["username"]
    password = user_credentials[i]["password"]
    bot.login(username, password)

    for j in range(0, randrange(int(MAX_POSTS_PER_USER))):
        post = bot.write_post(fake.text())
        post_ids.append(post["id"])

    for k in range(0, randrange(int(MAX_LIKES_PER_USER))):
        bot.like_post(choice(post_ids))
        