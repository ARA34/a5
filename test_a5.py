import ds_client as dsc
import ds_protocol as dsp
from Profile import Profile

# Send a directmessage to another DS user (in the example bellow, ohhimark)
# {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}



# create two people
def main():
    server_ip = "168.235.86.101"
    PORT = 3021

    melon_musk = Profile(dsuserver=server_ip, username="melonmusk", password="XA123")
    dsp.join(server=melon_musk.dsuserver,
                                port=PORT,
                                username=melon_musk.username,
                                password=melon_musk.password)


if __name__ == "__main__":
    main()