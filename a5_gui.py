import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
from ds_messenger import DirectMessenger
import ds_protocol as dsp
import file_handler as fh
import json
from Profile import Profile
import time
from pathlib import Path


class Body(tk.Frame):
    def __init__(self, root, recipient_selected_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = [str]
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()
        self.all_messages = None

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self._contacts[index]
        print(entry) # selected user
        if self._select_callback is not None:
            self._select_callback(entry)
            self.message_editor.delete(1.0, tk.END)
            # delete
            # self.message_editor.delete(1.0, tk.END)
            # TODO: insert messages here

    def insert_contact(self, contact: str):
        self._contacts.append(contact)
        id = len(self._contacts) - 1
        self._insert_contact_tree(id, contact)

    def _insert_contact_tree(self, id, contact: str):
        if len(contact) > 25:
            entry = contact[:24] + "..."
        id = self.posts_tree.insert('', id, id, text=contact)

    def insert_user_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-right')

    def insert_contact_message(self, message:str):
        self.entry_editor.insert(1.0, message + '\n', 'entry-left')

    def delete_contact_message(self, message: str):
        self.entry_editor.delete("1.0", len(message))

    def get_text_entry(self) -> str:
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)
    
    def delete_everything(self):
        print("delete...")
        self.message_editor.delete(1.0, tk.END)

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)

        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        editor_frame = tk.Frame(master=entry_frame, bg="red")
        editor_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        message_frame = tk.Frame(master=self, bg="yellow")
        message_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        self.message_editor = tk.Text(message_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                                 expand=True, padx=0, pady=0)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5)
        self.entry_editor.tag_configure('entry-right', justify='right')
        self.entry_editor.tag_configure('entry-left', justify='left')
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT,
                               expand=True, padx=0, pady=0)

        entry_editor_scrollbar = tk.Scrollbar(master=scroll_frame,
                                              command=self.entry_editor.yview)
        self.entry_editor['yscrollcommand'] = entry_editor_scrollbar.set
        entry_editor_scrollbar.pack(fill=tk.Y, side=tk.LEFT,
                                    expand=False, padx=0, pady=0)


class Footer(tk.Frame):
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        self.server_label = tk.Label(frame, width=30, text="DS Server Address")
        self.server_label.pack()

        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(tk.END, "")
        self.server_entry.pack()

        self.username_label = tk.Label(frame, width=30, text="Username")
        self.username_label.pack()

        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(tk.END, "")
        self.username_entry.pack()

        self.password_label = tk.Label(frame, width=30, text="Password")
        self.password_label.pack()

        self.password_entry = tk.Entry(frame, width=30)
        self.password_entry['show'] = '*'
        self.password_entry.insert(tk.END, "")
        self.password_entry.pack()

    def apply(self):
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()
        self.server = self.server_entry.get()


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        # You must implement this! You must configure and
        # instantiate your DirectMessenger instance after this line.
        #self.direct_messenger = ... continue!
        self.direct_messenger = None
        self.profile = None
        self.loaded = False
        # self.direct_messenger = DirectMessenger(dsuserver="168.235.86.101", username="melonmusk", password="XA123") #DirectMessenger(dsuserver=self.server, username=self.username, password=self.password)

        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the root frame
        self._draw()
        #self.body.insert_contact("studentexw23") # adding one example student.
        #self.body.insert_contact("melonmusk2") # adding two example student.
        # self.body.insert_contact_message("Welcome!") # example message

    def send_message(self):
        """
        Send a message to user if a profile is loaded
        """
        print("send pressed")
        print(f"server after pressed: {self.server}")
        message = self.body.get_text_entry()
        if self.server is None:
            print("WARNING: You must create new or load a profile first.")
            return
        else:
            dsp.dm(self.direct_messenger, message=message, recipient=self.recipient) # Message and Recipient working

    def add_contact(self):
        """
        Adds a contact.
        """
        # You must implement this!
        # Hint: check how to use tk.simpledialog.askstring to retrieve
        # the name of the new contact, and then use one of the body
        # methods to add the contact to your contact list
        if self.direct_messenger is None:
            print("WARNING: You must create or load a profile first")
            return
        else:
            contact = tk.simpledialog.askstring("Input", "Enter the name of a profile: ")
            self.body.insert_contact(contact)
            if contact not in self.profile.friends:
                self.profile.add_friend(contact)

    def recipient_selected(self, recipient):
        self.recipient = recipient
        self.body.delete_everything()
        recp = self.recipient
        valid_names = list(filter(lambda d: d[0] == recp, self.profile.all_messages))
        valid_msgs = list(map(lambda d: d[1], valid_names))
        for msg in valid_msgs:
            self.body.insert_contact_message(f"{recp}: {msg}")

    def configure_server(self):
        """
        Prompts the user to enter details to configure(change) server, username, and password.
        """
        if self.direct_messenger is None:
            print("WARNING: You must create or load a profile first")
            return
        else:
            ud = NewContactDialog(self.root)
            if ud.server != "":
                self.server = ud.server
                self.profile.dsuserver = ud.server
            if ud.user != "":
                self.username = ud.user
                self.profile.username = ud.user
            if ud.pwd != "":
                self.password = ud.pwd
                self.profile.password = ud.pwd
            print(f"Before config server: {self.profile}")
            self.profile.save_profile(fh.get_profile_path(self.direct_messenger.username))

        # if self.server is not None and self.username is not None and self.password is not None and self.direct_messenger is None:
        #     self.direct_messenger = DirectMessenger(dsuserver=self.server, username=self.username, password=self.password)
        #     self.profile = Profile(dsuserver=self.server, username=self.username, password=self.password)
        #     # check if user has already been created
        #     if fh.user_exists(self.direct_messenger.username):
        #         pass
        #     else:
        #         fh.create_profile(self.direct_messenger)
        #     self.profile = Profile()
        #     self.profile.load_profile(fh.get_profile_path(self.direct_messenger.username))
        #     self.load_assets()

    def publish(self, message:str):
        # You must implement this!
        pass
        # dsp.post(self.direct_messenger, message=message)

    def check_new(self):
        """
        Checks for new messages every 2 seconds.
        """
        # print(f"self_direct: {self.direct_messenger}") # this is None
        # print(f"self_profile: {self.profile}")

        # its not entering this if because self.direct_messenger is None

        dsm_var = self.direct_messenger
        # print(f"dsm: {dsm_var}")

        if self.loaded is True:
            continue_check = dsm_var.join()
            if continue_check:
                message_tup_lst = dsm_var.retrieve_new() # is getting [(user, message)]
                print(f"General Message: {message_tup_lst}")
                if len(message_tup_lst) >= 1:
                    for tup in message_tup_lst:
                        print(f"msg: {tup[1]}, sender: {tup[0]}")
                        self.body.insert_contact_message(tup[0] + ": " + tup[1])
                    if self.profile is not None:
                        self.profile.set_new_messages()
            else:
                print("Could not connect to sever - check_new")
                self.body.insert_contact_message("WARNING: You must create or load a profile first")
        else:
            pass
        self.root.after(2000, self.check_new)


        # tmp_var = self.direct_messenger
        # if tmp_var is not None:
        #     continue_check = tmp_var.join()
        #     # time.sleep(1) # debug
        #     if continue_check is True:
        #         message = tmp_var.retrieve_new()
        #         print(f"msg: {message}, len: {len(message)}") # debug
        #         if len(message) >= 1:
        #             self.body.insert_contact_message(message[0])
        #         # else:
        #         #     self.body.insert_contact_message("Waiting for messages...")
        #         #     self.body.delete_contact_message("waiting for messages...")
        #             if self.profile is not None:
        #                 self.profile.set_new_messages()
        #         self.root.after(2000, self.check_new)
        #     else:
        #         self.body.insert_contact_message("WARNING: You must create or load a profile first")

    def open_file(self) -> None:
        """
        Opens a file and reads the contents of the file. Loads an exisitng profile on local device to server.
        """
        file_path = filedialog.askopenfilename()
        if Path(file_path).suffix == ".dsu":
            file_read = open(file_path, mode="r", encoding="utf-8")
            text_data = file_read.read()
            file_read.close()
            text_data = json.loads(text_data)
            print(f"text_data: {text_data}")
            self.server = text_data["dsuserver"]
            self.username = text_data["username"]
            self.password = text_data["password"]
            if self.server is not None and self.username is not None and self.password is not None and self.direct_messenger is None:
                self.direct_messenger = DirectMessenger(dsuserver=self.server, username=self.username, password=self.password)
                print(self.direct_messenger)
                self.profile = Profile()
                self.profile.load_profile(str(file_path))
                self.load_assets()
                self.loaded = True
        else:
            print("Wrong File. Please select a DSU file.")

    def new_profile(self) -> None:
        """
        Creates new profile and connects to ICS32 distributed social website
        """
        ud1 = NewContactDialog(self.root, title="Creating ICS32 Distributed Account")
        s_prof = Profile(dsuserver=ud1.server, username=ud1.user, password=ud1.pwd)
        if fh.user_exists(s_prof.username):
            pass
        else:
            fh.create_profile(s_prof)

    def load_assets(self) -> None:
        print("load")
        if self.profile is not None and self.direct_messenger is not None:
            if self.direct_messenger.join() is True:
                for friend in self.profile.friends:
                    self.body.insert_contact(friend)
                # recp = self.recipient

                # valid_msgs = list(filter(lambda d: d[0] == recp, self.profile.all_messages))

                # for msg in valid_msgs:
                #     print(f"{recp}: {msg}")
                #     self.body.insert_contact_message(recp + ": " + msg)
        self.loaded = True

                # for message in self.profile.all_messages:
                #     self.body.insert_contact_message(message)

    def close_window(self) -> None:
        """
        Closes GUI and saves user information onto local machine
        """
        print(f"profile: {self.profile}")
        self.profile.set_all_messages() # error because dsu sever invalid -> pass the error
        time.sleep(1) # buffer to load
        fh.store_profile(self.profile)
        self.root.destroy()

    def _draw(self):
        """
        Builds a menu and adds it to the frame
        """
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)

        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_file)
        menu_file.add_command(label='Close', command=self.close_window)

        settings_file = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings_file, label='Settings')
        settings_file.add_command(label='Add Contact',
                                  command=self.add_contact)
        settings_file.add_command(label='Configure DS Server',
                                  command=self.configure_server)

        # The Body and Footer classes must be initialized and
        # packed into the root window.
        self.body = Body(self.root,
                         recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)

# def main_func():
if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    # login = tk.Tk()
    # login_win = NewContactDialog(login, title="login window")

    main = tk.Tk()
    login_win = NewContactDialog(main, title="login window")
    # these are all set
    log_server = login_win.server
    log_user = login_win.user
    log_pass = login_win.pwd

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value
    # around to see how the starting size of the window changes.
    main.geometry("720x480")

    # adding this option removes some legacy behavior with menus that
    # some modern OSes don't support. If you're curious, feel free to comment
    # out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the
    # widgets used in the program. All of the classes that we use,
    # subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.

    app = MainApp(main)
    app.direct_messenger = DirectMessenger(dsuserver=log_server, username=log_user, password=log_pass)
    app.profile = Profile()
    app.profile.load_profile(fh.get_profile_path(app.direct_messenger.username))
    app.load_assets()

    # When update is called, we finalize the states of all widgets that
    # have been configured within the root frame. Here, update ensures that
    # we get an accurate width and height reading based on the types of widgets
    # we have used. minsize prevents the root window from resizing too small.
    # Feel free to comment it out and see how the resizing
    # behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(f"ID: {id}")
    # And finally, start up the event loop for the program (you can find
    # more on this in lectures of week 9 and 10).
    main.mainloop()
