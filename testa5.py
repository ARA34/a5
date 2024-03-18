import ds_protocol as dsp
from Profile import Profile
import ds_messenger as dsm
import time

# Send a directmessage to another DS user (in the example bellow, ohhimark)
# {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}



# create two people

def main():
    server_ip = "168.235.86.101"
    PORT = 3021

    # melon_musk = Profile(dsuserver=server_ip, username="melonmusk", password="XA123")
    # dsp.join(server=melon_musk.dsuserver,
    #                             port=PORT,
    #                             username=melon_musk.username,
    #                             password=melon_musk.password)
    # melon_musk_2 = Profile(dsuserver=server_ip, username="melonmusk2", password="XA123")
    # dsp.join(server=melon_musk_2.dsuserver,
    #                             port=PORT,
    #                             username=melon_musk_2.username,
    #                             password=melon_musk_2.password)
    
    # json_str = {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
    # dsp.post(server=melon_musk_2.dsuserver,
    #                             port=PORT,
    #                             username=melon_musk_2.username,
    #                             password=melon_musk_2.password,
    #                             message="bruhreally21")
    
    # print(dsp.dm(server=server_ip, port=PORT, username=melon_musk.username, password=melon_musk.password, message="new", extra="melonmusk2"))
    # print(dsp.request_messages(server=server_ip, port=PORT, username=melon_musk_2.username, password=melon_musk_2.password, extra="new"))
    
    # DM: melonmusk --> melonmusk2
    # print(dsp.dm(server="168.235.86.101", port=PORT, username=melon_musk.username, password=melon_musk.password, message="hello there", extra="melonmusk2"))

    melonmusk_dsm = dsm.DirectMessenger(server_ip, "melonmusk", "XA123")
    melonmusk_dsm.join() # melonmusk needs to join server first
    message = "-_- again twice"
    if melonmusk_dsm.send(message=message, recipient="melonmusk3") is True:
        print(f"Sent message: {message}")
    else:
        print("failed to send message")
    # while True:
    #     time.sleep(2)
    #     print(f"Recieved: {melonmusk_dsm.retrieve_new()}")

    # print(f"sent message: {}") # sending dm 1
    # melonmusk_dsm.send(message = "5", recipient="melonmusk2") # sending dm 2
    # melonmusk_dsm.send(message = "6", recipient="melonmusk2") # sending dm 2
    
    # melonmusk2_dsm = dsm.DirectMessenger(server_ip, "melonmusk2", "XA123")
    # print(melonmusk2_dsm.send(message="",recipient="new")) # recieving dm, sets data to (new messages)
    # print(f"recieved: {melonmusk2_dsm.retrieve_new()}")

if __name__ == "__main__":
    main()