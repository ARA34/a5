"""
Testing ds_messenger.py
"""
from ds_messenger import *

DSUSERVER = "168.235.86.101"


# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988


melonmusk = DirectMessenger(dsuserver=DSUSERVER,
                            username="melonmusk",
                            password="XA123")


def test_join():
    """
    Tests joining capabilities for DirectMessenger object
    """
    assert melonmusk.join() is True


def test_dm():
    """
    Tests direct message functionality from
    """
    assert melonmusk.send(message="16",
                          recipient="melonmusk2") is True


def test_retrieve_all():
    """
    Tests retrive all from direct messenger
    """
    melonmusk2 = DirectMessenger(dsuserver=DSUSERVER,
                                 username="melonmusk2",
                                 password="XA123")
    assert melonmusk2.retrieve_all() is not None


def test_retrivew_new():
    """
    Tests retrieve all from direct messenger
    """
    melonmusk2 = DirectMessenger(dsuserver=DSUSERVER,
                                 username="melonmusk2",
                                 password="XA123")
    assert melonmusk2.retrieve_new() is not None
