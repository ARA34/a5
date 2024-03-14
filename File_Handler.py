from pathlib import Path
from Profile import *
import ds_protocol as dsp
import time

current_folder = Path(".").resolve()

def create_profile_folder() -> str:
    """
    Creates a folder for dsu_profiles and returns the name of the path to get there.
    """
    folder_name = "dsu_profiles"
    new_path = current_folder / folder_name
    if not new_path.exists():
        new_path.mkdir(parents=True, exist_ok=True)
    return str(new_path)

def store_profile(profile: Profile):
    folder_path = Path(create_profile_folder())
    extension = profile.username + ".dsu"
    new_path = folder_path / extension
    new_path.touch()
    profile.save_profile(path=new_path)

# structure for saving messages
p1 = Profile(dsuserver="168.235.86.101", username="melonmusk2", password="XA123")
melonmusk_dsm = DirectMessenger("168.235.86.101", "melonmusk", "XA123")
melonmusk_dsm.send(message="16", recipient="melonmusk2") # sending dm 1
p1.set_new_messages()
p1.set_all_messages()
time.sleep(1)
store_profile(p1)