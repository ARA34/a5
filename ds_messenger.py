import socket
import json
import time
from collections import namedtuple


# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988


PORT = 3021
OK = "ok"
ERROR = "error"
Connection = namedtuple("Connection", ["socket", "send", "recv"])
msg_info = namedtuple('msg_info', ['type', 'message', 'token'])


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

        message_list = json_obj["response"][m]
        msg_info_1 = msg_info(type, message_list, "")
        if len(vals) == 3:
            # token exists
            token = json_obj["response"]["token"]
            msg_info_1 = msg_info(type, message_list, token)
    except json.JSONDecodeError:
        print("Json cannot be decoded.")
    return msg_info_1


class DirectMessage:

    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None

    def set_recipient(self, recipient: str) -> None:
        """
        sets the recipient attribute
        """
        self.recipient = recipient

    def set_message(self, message: str) -> None:
        """
        sets the message attribute
        """
        self.message = message

    def get_recipient(self):
        return self.recipient

    def get_message(self):
        return self.message

    def format_dm(self, token):
        """
        formats json_msg so that it can
        send a dm or request the latest dm or all the dms
        """
        if self.recipient == "new":
            json_msg = {"token": token, "directmessage": "new"}
        elif self.recipient == "all":
            json_msg = {"token": token, "directmessage": "all"}
        else:
            json_msg = {"token": token,
                        "directmessage": {"entry": self.message,
                                          "recipient": self.recipient,
                                          "timestamp":
                                          str(time.time())}}
        return json_msg


class DirectMessenger:

    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None

        self.dsuserver = dsuserver
        self._conn = None

        self.username = username
        self.password = password
        self.bio = ""
        self.data = None

    def get_conn(self) -> None:
        """
        Sets _conn connection attribute
        """
        return self._conn

    def set_bio(self, bio: str) -> None:
        """
        sets bio attribute
        """
        self.bio = bio

    def get_details(self):
        """
        For debugging, prints all class information
        """
        print(self.dsuserver)
        print(self.username)
        print(self.password)
        print(self.token)
        print(self.data)
        print(self._conn)

    def send(self, message: str, recipient: str) -> bool:
        """
        General sending function to commuicate with server.
        must return true if message successfully sent,
        false if send failed.
        """
        try:
            sock = self.connect_server(self.dsuserver, PORT)
            if sock is None:
                print("Couldn't connect to server")
                return
            self.init_conn(sock)
            self.set_token()
            sending_two = False

            if ((self.username and self.password != "")
                and (message == "")
                and self.bio == ""
                and recipient is None):
                # joining server
                json_msg = {"join":
                            {"username": self.username,
                             "password": self.password,
                             "token": ""}}
            elif (message != ""
                  and self.bio is None
                  and recipient is None):
                # posting message
                json_msg = {"token": self.token,
                            "post": {"entry":
                                     message,
                                     "timestamp": str(time.time())}}
            elif (message == ""
                  and self.bio != ""
                  and recipient is None):
                # changing bio
                json_msg = {"token": self.token,
                            "bio": {"entry":
                                    self.bio,
                                    "timestamp":
                                    str(time.time())}}
            elif recipient is not None:
                # sending dm (to recipient) or recieving dm(s)(for you)
                direct_message = DirectMessage()
                direct_message.set_recipient(recipient)
                direct_message.set_message(message)
                json_msg = direct_message.format_dm(self.token)

            elif message != "" and self.bio != "":
                sending_two = True

            if sending_two:
                json_msg_1 = {"token": self.token,
                              "post": {"entry":
                                       message,
                                       "timestamp":
                                       str(time.time())}}
                json_msg_2 = {"token": self.token,
                              "bio": {"entry":
                                      self.bio,
                                      "timestamp":
                                      str(time.time())}}
                json_msg_1 = json.dumps(json_msg_1)
                self.write_command(json_msg_1)
                response_1 = self.read_command()
                parsed_r1 = extract_json(response_1)
                resp_1_type = parsed_r1.type
                json_msg_2 = json.dumps(json_msg_2)
                self.write_command(json_msg_2)
                response_2 = self.read_command()
                parsed_r2 = extract_json(response_2)
                resp_2_type = parsed_r2.type
                if resp_1_type == OK and resp_2_type == OK:
                    satisfy = OK
                else:
                    satisfy = ERROR
            else:
                json_msg = json.dumps(json_msg)
                self.write_command(json_msg)
                response = self.read_command()
                parsed_resp = extract_json(response)
                self.data = parsed_resp.message
                satisfy = parsed_resp.type
            if satisfy == OK:
                return True
            elif parsed_resp.type == ERROR:
                return False
        except Exception as ex:
            return ("An error occured while sending. ", ex)

    def join(self):
        """
        joins user
        """
        return self.send(message="", recipient=None)

    def retrieve_new(self) -> list:
        """
        Retrives list of new messages being sent to user
        """
        self.send(message="",
                  recipient="new")
        dict_messages = self.data
        output_messages = list(map(lambda d: d["message"],
                                   dict_messages))
        users = list(map(lambda d: d["from"], dict_messages))
        output_list = list(map(lambda x, y: (x, y),
                               users, output_messages))
        output_list_2 = []
        for tup in output_list:
            n = DirectMessage()
            n.set_recipient(tup[0])
            n.set_message(tup[1])
            output_list_2.append(n)
        return output_list_2

    def retrieve_all(self) -> list:
        """
        retrives all messages ever to be sent to this user as well as senders
        """
        self.send(message="", recipient="all")
        try:
            dict_messages = self.data
            output_messages = list(map(lambda d: d["message"],
                                       dict_messages))
            users = list(map(lambda d: d["from"],
                             dict_messages))
            output_list = list(map(lambda x, y: (x, y),
                                   users, output_messages))
            output_list_2 = []
            for tup in output_list:
                n = DirectMessage()
                n.set_recipient(tup[0])
                n.set_message(tup[1])
                output_list_2.append(n)
            return output_list_2
        except Exception as ex:
            print(f"Error, something wrong, {ex}")
            return

    def init_conn(self, sock: socket) -> None:
        """
        Creates a named tuple to organize
        client-side connection
        """
        try:
            f_send = sock.makefile("w")
            f_recv = sock.makefile("r")
        except Exception as ex:
            print(f"init_conn: {ex}")
        self._conn = Connection(
            socket=sock,
            send=f_send,
            recv=f_recv
          )

    def write_command(self, cmd: str):
        """
        Pushes information to server
        """
        try:
            self.get_conn().send.write(cmd + "\r\n")
            self.get_conn().send.flush()
        except Exception as ex:
            print(f"write_command: {ex}")

    def read_command(self) -> str:
        """
        Gets information from server
        """
        cmd = self.get_conn().recv.readline()
        return cmd

    def connect_server(self, host: str, port: int):
        """
        Connects to the server using sockets
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            return sock
        except Exception as ex:
            print(f"connect_server: {ex}")
            return None

    def set_token(self) -> None:
        join_msg = {"join":
                    {"username": self.username,
                     "password": self.password,
                     "token": ""}}
        join_msg = json.dumps(join_msg)
        self.write_command(join_msg)
        resp = self.read_command()
        parsed_resp = extract_json(resp)
        self.token = str(parsed_resp.token)
