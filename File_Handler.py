from pathlib import Path
from Profile import *
import ds_protocol as dsp
import time
import ds_messenger as dsm


# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988


current_folder = Path(".").resolve()


def create_profile_folder() -> str:
    """
    Creates a folder for dsu_profiles and returns
    the name of the path to get there.
    """
    folder_name = "dsu_profiles"
    new_path = current_folder / folder_name
    if not new_path.exists():
        new_path.mkdir(parents=True, exist_ok=True)
    return str(new_path)


def create_profile(profile: Profile):
    """
    Creates a new profile and returns the instance of the profile.
    """
    new_profile = Profile(dsuserver=profile.dsuserver,
                          username=profile.username,
                          password=profile.password)
    store_profile(new_profile)


def user_exists(username: str):
    """
    checks if a user profile exists
    """
    return (current_folder / "dsu_profiles" / (username + ".dsu")).exists()


def get_profile_path(username: str) -> str:
    """
    returns the path to profile in a string
    """
    if user_exists(username):
        return str(current_folder / "dsu_profiles" / (username + ".dsu"))
    else:
        print("ERROR: User does not exists, create new or load first")


def store_profile(profile: Profile):
    """
    Stores the profile in the dsu_profiles folder.
    """
    folder_path = Path(create_profile_folder())
    extension = profile.username + ".dsu"
    new_path = folder_path / extension
    new_path.touch()
    profile.save_profile(path=new_path)


def get_messages_in_file(username: str):
    folder_path = Path(".").resolve()
    dsu_folder = folder_path / "dsu_profiles"
    if dsu_folder.exists():
        user_path = folder_path / "dsu_profiles" / (username + ".dsu")
        file_read = open(user_path, mode="r", encoding="utf-8")
        text_data = file_read.read()
        file_read.close()

        text_data = json.loads(text_data)
        return text_data
    else:
        print("There is no dsu profile folder")
