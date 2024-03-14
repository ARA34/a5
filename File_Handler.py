from pathlib import Path

current_folder = Path(".").resolve()

def create_profile_folder():
    folder_name = "profiles"
    new_path = current_folder / folder_name
    if not new_path.exists:
        new_path.mkdir()
    
create_profile_folder()