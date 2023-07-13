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