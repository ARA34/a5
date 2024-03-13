# Starter code for assignment 3 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your
# information.

# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988


import socket
import ds_protocol as dsp
import json
import time
from typing import Callable
from collections import namedtuple


Connection = namedtuple("Connection", ["socket", "send", "recv"])


def init(sock: socket) -> Connection:
    try:
        f_send = sock.makefile("w")
        f_recv = sock.makefile("r")
    except Exception:
        raise dsp.DSPServerError
    return Connection(
        socket=sock,
        send=f_send,
        recv=f_recv
      )


def write_command(_conn: Connection, cmd: str):
    try:
        _conn.send.write(cmd + "\r\n")
        _conn.send.flush()
    except Exception:
        raise dsp.DSPServerError


def read_command(_conn: Connection) -> str:
    cmd = _conn.recv.readline()
    return cmd


def connect_to_server(host: str, port: int) -> socket.socket:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
    except Exception:
        return None


def send(server: str, port: int, username: str,
         password: str, message: str, extra: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    try:
        sock = connect_to_server(server, port)
        if sock is None:
            print("couldn't connect to server")
            return
        _conn = init(sock)
        json_msg = ""
        usr_token = get_token(_conn, username, password)

        sending_two = False
        if (username and password != "") and (message == "") and bio is None and extra is None:
            json_msg = {"join":
                        {"username": username,
                         "password": password,
                         "token": ""}}
        elif message != "" and bio is None and extra is None:
            json_msg = {"token": usr_token,
                        "post": {"entry": message,
                                 "timestamp": str(time.time())}}
        elif message == "" and bio != "" and extra is None:
            json_msg = {"token": usr_token,
                        "bio": {"entry": bio,
                                "timestamp": str(time.time())}}
        elif extra is not None:
            # either direct message sending or requesting
            if extra == "new":
                json_msg = {"token":usr_token, "directmessage": "new"}
            elif extra == "all":
                json_msg = {"token":usr_token, "directmessage": "all"}
            else:
                json_msg = {"token":usr_token,
                            "directmessage": {"entry": message,
                                              "recipient":extra,
                                              "timestamp": str(time.time())}}
        elif message != "" and bio != "":
            sending_two = True
        else:
            print("something went wrong.")
        if sending_two:
            json_msg_1 = {"token": usr_token,
                          "post": {"entry": message,
                                   "timestamp": str(time.time())}}
            json_msg_2 = {"token": usr_token,
                          "bio": {"entry": bio,
                                  "timestamp": str(time.time())}}
            json_msg_1 = json.dumps(json_msg_1)
            write_command(_conn, json_msg_1)
            response_1 = read_command(_conn)
            parsed_r1 = dsp.extract_json(response_1)
            resp_1_type = parsed_r1.type

            json_msg_2 = json.dumps(json_msg_2)
            _conn2 = init(sock)
            write_command(_conn2, json_msg_2)
            response_2 = read_command(_conn2)
            parsed_r2 = dsp.extract_json(response_2)
            resp_2_type = parsed_r2.type
            if resp_1_type == dsp.OK and resp_2_type == dsp.OK:
                satisfy = dsp.OK
            else:
                satisfy = dsp.ERROR
        else:
            json_msg = json.dumps(json_msg)
            write_command(_conn, json_msg)
            response = read_command(_conn)
            parsed_resp = dsp.extract_json(response)
            satisfy = parsed_resp.type
        if satisfy == dsp.OK:
            return True
        elif parsed_resp.type == dsp.ERROR:
            return False
    except Exception as ex:
        return ("An error occured while sending. ", ex)


def get_token(_conn: Connection, username: str, password: str) -> str:
    join_msg = {"join":
                {"username": username,
                 "password": password,
                 "token": ""}}
    join_msg = json.dumps(join_msg)
    write_command(_conn, join_msg)
    resp = read_command(_conn)
    parsed_resp = dsp.extract_json(resp)
    return str(parsed_resp.token)
