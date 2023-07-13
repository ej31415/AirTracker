import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.simpledialog as tksd

def add_email():
    email = tksd.askstring(title='Add Email', prompt="What is your email? ")
    try:
        if (email + "\n") in open('recipients.txt', 'r').readlines():
            tkmsg.showinfo("Notice", email + " is already on the recipient list.")
            return
    except IOError:
        pass
    with open("recipients.txt", 'a+') as track_list:
        track_list.write(email + "\n")
        tkmsg.showinfo("Tracking! ", "Added " + email + " for tracked flights notifications.")

def delete_email():
    email = tksd.askstring(title='Delete Email', prompt="What is your email? ")
    try:
        with open("recipients.txt", "r") as rList:
            recipients = rList.readlines()
        if (email + "\n") not in recipients:
            tkmsg.showinfo("Notice", email + " is not on the recipient list.")
            return
        else: 
            with open("recipients.txt", "w+") as rList:
                for recipient in recipients:
                    if recipient[:-1] != email:
                        rList.write(recipient)
            tkmsg.showinfo("Success", email + " has been deleted!")
    except IOError:
        return

def clear_emails():
    with open("recipients.txt", "w+") as to_clear:
        pass
    tkmsg.showinfo("Success", "All emails cleared from recipients list.")

def view_emails():
    txt = ""
    try:
        for email in open("recipients.txt", 'r').readlines():
            txt += email
    except IOError:
        pass
    if txt == "":
        txt = "No recipients yet!"
    tkmsg.showinfo("Recipients", txt)