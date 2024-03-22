
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
import ds_messenger as dsm

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
        keys = list(json_obj["response"].keys())
        if "message" in keys:
            m = "message"
        elif "messages" in keys:
            m = "messages"
        type = json_obj["response"]["type"]
        message = json_obj["response"][m]
        msg_info_1 = msg_info(type, message, "")
        if len(vals) == 3:
            token = json_obj["response"]["token"]
            msg_info_1 = msg_info(type, message, token)
    except json.JSONDecodeError:
      print("Json cannot be decoded.")
    return msg_info_1


def join(dsm_object: dsm.DirectMessenger):
    """
    Connects and joins user to server.
    """
    username = dsm_object.username.strip()
    if username != "" and len(username) > 1:
        return dsm_object.join()
    else:
        print(f"A username cannot be only whitespaces, empty, or a single character. Please try again.")
 

def post(dsm_object: dsm.DirectMessenger, message: str):
    """
    Posts user's messages on server.
    """
    message = message.strip()
    if message != "" and len(message) > 1:
        print(f"Your message [{message}] was posted")
        dsm_object.send(message=message, recipient=None)
    else:
        print("You cannot post empty or whitespace only posts or single character. Please Try again.")


def bio(dsm_object: dsm.DirectMessenger, bio: str):
    """
    Changes user's bio
    """
    bio = bio.strip()
    if bio != "" and len(bio) > 1:
        print(f"Your bio was changed to [{bio}]")
        dsm_object.set_bio(bio)
        dsm_object.send(message="", recipient=None)
    else:
        print("You cannot have an empty or only whitespace bio or single character. Please try again.")
        dsm_object.send(message="", recipient=None)


def dm(dsm_object: dsm.DirectMessenger, message: str, recipient: str):
    """
    Sends a direct message
    """
    message = message.strip()
    if message != "" and len(message) > 1:
        return dsm_object.send(message=message, recipient=recipient)
    else:
        print("You cannot post empty or whitespace only posts or single character. Please Try again.")


def request_messages(dsm_object: dsm.DirectMessenger, recipient: str):
    """
    Extracs new or all message(s)
    """
    if recipient == "new" or recipient == "all":
        if recipient == "new":
            dsm_object.retrieve_new()
        elif recipient == "all":
            dsm_object.retrieve_all()
    else:
        print("Can only enter 'new' or 'all' for recipient parameter")
        return False
