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
    melon_musk_2 = Profile(dsuserver=server_ip, username="melonmusk2", password="XA123")
    dsp.join(server=melon_musk_2.dsuserver,
                                port=PORT,
                                username=melon_musk_2.username,
                                password=melon_musk_2.password)
    
    # json_str = {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
    # dsp.post(server=melon_musk_2.dsuserver,
    #                             port=PORT,
    #                             username=melon_musk_2.username,
    #                             password=melon_musk_2.password,
    #                             message="bruhreally21")
    
    print(dsp.dm(server=server_ip, port=PORT, username=melon_musk.username, password=melon_musk.password, message="new", extra="melonmusk2"))
    print(dsp.request_messages(server=server_ip, port=PORT, username=melon_musk_2.username, password=melon_musk_2.password, extra="new"))
    
    # DM: melonmusk --> melonmusk2
    # print(dsp.dm(server="168.235.86.101", port=PORT, username=melon_musk.username, password=melon_musk.password, message="hello there", extra="melonmusk2"))

if __name__ == "__main__":
    main()