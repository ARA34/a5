from ds_messenger import *

DSUSERVER = "168.235.86.101"

def dsm_join():
    melonmusk = DirectMessenger(dsuserver=DSUSERVER, username="melonmusk", password="XA123")
    assert melonmusk.send(message="", recipient=None) is True