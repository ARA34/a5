
# Starter code for assignment 3 in ICS 32 
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988

from __future__ import annotations
import json
from collections import namedtuple
import socket
import Profile
import time
import ds_client as dsc

class DSPServerError(Exception):
  pass


msg_info = namedtuple('msg_info', ['type','message','token'])


JOIN = "join"
BIO = "bio"
POST = "post"


ERROR = "error"
OK = "ok"


def extract_json(json_msg: str) -> msg_info:
    '''
    Call the json.loads function on a json string and
    convert it to a DataTuple object
    Input: json_string
    Output: namedtuple with parts of json string
    '''
    try:
        json_obj = json.loads(json_msg)
        vals = list(json_obj["response"].values())
        type = json_obj["response"]["type"]
        message = json_obj["response"]["message"]
        msg_info_1 = msg_info(type, message, "")
        if len(vals) == 3:
            token = json_obj["response"]["token"]
            msg_info_1 = msg_info(type, message, token)
    except json.JSONDecodeError:
      print("Json cannot be decoded.")
    return msg_info_1


def join(server: str, port: int, username: str, password: str, token=""):
    username = username.strip()
    if username != "" and len(username) > 1:
        return dsc.send(server=server, port=port, username=username, password=password, message="", bio=None)
    else:
        print(f"A username cannot be only whitespaces, empty, or a single character. Please try again.")
 

def post(server: str, port: int, username: str, password: str, message: str):
    message = message.strip()
    if message != "" and len(message) > 1:
        print(f"Your message [{message}] was posted")
        return dsc.send(server=server, port=port, username=username, password=password, message=message)
    else:
        print("You cannot post empty or whitespace only posts or single character. Please Try again.")
        return False


def bio(server: str, port: int, username: str, password: str, bio: str):
    bio = bio.strip()
    if bio != "" and len(bio) > 1:
        print(f"Your bio was changed to [{bio}]")
        return dsc.send(server=server, port=port, username=username, password=password, message ="", bio=bio)
    else:
        print("You cannot have an empty or only whitespace bio or single character. Please try again.")
        return dsc.send(server=server, port=port, username=username, password=password, message="", bio=bio)
