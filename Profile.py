from pathlib import Path
from ds_messenger import *


# Alex Reyes Aranda
# areyesar@uci.edu
# 69754988


"""
DsuFileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler that you should catch in your own code. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Post(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently 
    supports two features: A timestamp property that is set upon instantiation and 
    when the entry object is set and an entry property that stores the post message.

    """
    def __init__(self, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and 
    time values. When the value for entry is changed, or set, the timestamp field is 
    updated to the current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)

class Profile:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ""
        self._posts = []

        self.friends = []
        self.new_messages = []
        self.all_messages = []

    def set_dsu(self, server: str) -> None:
        self.dsuserver = server

    def set_user(self, user: str) -> None:
        self.username = user

    def set_pass(self, password: str) -> None:
        self.password = password

    def add_friend(self, friend: str) -> None:
        self.friends.append(friend)
    
    """

    add_post accepts a Post object as parameter and appends it to the posts list. Posts 
    are stored in a list object in the order they are added. So if multiple Posts objects 
    are created, but added to the Profile in a different order, it is possible for the 
    list to not be sorted by the Post.timestamp property. So take caution as to how you 
    implement your add_post code.

    """

    def add_post(self, post: Post) -> None:
        self._posts.append(post)

    """

    del_post removes a Post at a given index and returns True if successful and False if 
    an invalid index was supplied. 

    To determine which post to delete you must implement your own search operation on 
    the posts returned from the get_posts function to find the correct index.

    """

    def del_post(self, index: int) -> bool:
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False
        
    """
    
    get_posts returns the list object containing all posts that have been added to the 
    Profile object

    """
    def get_posts(self) -> list[Post]:
        return self._posts

    """

    save_profile accepts an existing dsu file to save the current instance of Profile 
    to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """

    def set_new_messages(self):
        """
        Uses the function from ds_messenger to retrieve new messages.
        """
        dsm = DirectMessenger(dsuserver=self.dsuserver,username=self.username,password=self.password)
        self.new_messages = dsm.retrieve_new()
    
    def set_new_messages_offline(self, messages:list):
        print("extended new_msgs")
        self.new_messages.extend(messages)
        

    def set_all_messages(self):
        """
        Uses the function from ds_messenger to retrieve all messages.
        """
        dsm = DirectMessenger(dsuserver=self.dsuserver,username=self.username,password=self.password)
        if dsm.join():
            self.all_messages = dsm.retrieve_all()
            new_list = []
            for i in self.all_messages:
                new_list.append([i.get_recipient, i.get_message])
            self.all_messages = new_list
        else:
            self.all_messages = self.all_messages

    def save_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a 
    DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                print(f"type: {type(f).__name__}")
                obj = json.load(f) # converts string to json dict
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.friends = obj["friends"]
                self.new_messages = obj["new_messages"]
                self.all_messages = obj["all_messages"]


                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
