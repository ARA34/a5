from ds_messenger import *
import ds_protocol as dsp

DSUSERVER = "168.235.86.101"


melonmusk = DirectMessenger(dsuserver=DSUSERVER, username="melonmusk", password="XA123")

def test_join():
    assert dsp.join(dsm_object=melonmusk) is True


def test_dm():
    assert dsp.dm(dsm_object=melonmusk, message="16", recipient="melonmusk2") is True


def test_retrieve():
    melonmusk2 = DirectMessenger(dsuserver=DSUSERVER, username="melonmusk2", password="XA123")
    assert melonmusk2.retrieve_all() is not None
