"""
Testing ds_protocol.py
"""
import ds_protocol as dsp
import ds_messenger as dsm


# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988


dsm_obj = dsm.DirectMessenger(dsuserver="168.235.86.101",
                              username="melonmusk4",
                              password="XA123")


def test_dm():
    """
    Tests dm from dsp
    """
    assert dsp.dm(dsm_object=dsm_obj,
                  message="example message",
                  recipient="melonmusk3") is True


def test_recieve_new_message():
    """
    Tests recieve_new from dsp
    """
    assert dsp.request_messages(dsm_object=dsm_obj,
                                recipient="new") is not False


def test_recieve_all_messages():
    """
    Tests recieve_all from dsp
    """
    assert dsp.request_messages(dsm_object=dsm_obj,
                                recipient="all") is not False
