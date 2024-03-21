import ds_protocol as dsp
import ds_messenger as dsm

dsm_obj = dsm.DirectMessenger(dsuserver="168.235.86.101", username="melonmusk4", password="XA123")

def test_dm():
    assert dsp.dm(dsm_object=dsm_obj, message="example message", recipient="melonmusk3") is True