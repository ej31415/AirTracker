import tkinter as tk
import tkinter.messagebox as tkmsg
import pandas as pd
import back
import interface.emails as iEm

initial_data = back.start_program()

root = tk.Tk()

root.title("AirTracker V1")
root.geometry('972x750')

menu = tk.Menu(root)
file = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=file)
file.add_command(label='Close Program', command=root.destroy)
notifs = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Notifications', menu=notifs)
notifs.add_command(label='Add Email', command=iEm.add_email)
notifs.add_command(label='View Mailing List', command=iEm.view_emails)
notifs.add_command(label="Delete Email", command=iEm.delete_email)
notifs.add_separator()
notifs.add_command(label='Clear Mailing List', command=iEm.clear_emails)
root.config(menu=menu)

header = tk.Label(root, text="Flight Tracking")
header.grid(row=0, column=0, padx=1, pady=2)

def set_search():
    choice = search_choice.get()
    if choice == 'Departure (Name)':
        return 1
    elif choice == 'Departure (IATA)':
        return 2
    elif choice == 'Arrival (Name)':
        return 3
    elif choice == 'Arrival (IATA)':
        return 4
    elif choice == 'Airline':
        return 5
    elif choice == 'Flight #':
        return 6
    return 0

def click_search():
    output.configure(state="normal")
    search_code = set_search()
    user_input = search_term.get()
    res = "Searching for " + user_input
    lblSearch.configure(text = res)
    output.delete('0.0', tk.END)
    output.insert(tk.END, back.display(user_input, search_code))
    output.configure(state="disabled")

def update_options(x):
    options = back.get_data_list(set_search())
    search_term.set('')
    enterSearch['menu'].delete(0, 'end')
    for option in options:
        enterSearch['menu'].add_command(label=option, command=tk._setit(search_term, option))

lblSearch = tk.Label(root, text="Search using departure airport (name/iata), arrival airport (name/iata), airline, or flight number (iata).")
lblSearch.grid(row=1, column=0, padx=1, pady=2)
search_list = ['Departure (Name)', 'Departure (IATA)', 'Arrival (Name)', 'Arrival (IATA)', 'Airline', 'Flight #']
search_choice = tk.StringVar()
search_choice.set('Choose Category')
search_dropdown = tk.OptionMenu(root, search_choice, *search_list, command=update_options)
search_dropdown.grid(row=2, column=0)
search_term = tk.StringVar()
search_term.set('---')
enterSearch = tk.OptionMenu(root, search_term, [])
enterSearch.grid(row=3, column=0, padx=1, pady=2)
btnSearch = tk.Button(root, text="Search", fg="red", command=click_search)
btnSearch.grid(row=4, column=0, padx=1, pady=2)
output = tk.Text(root, height=30, width=80, wrap=tk.WORD)
output.grid(row=5, column=0, columnspan=2, padx=1, pady=2)
output.config(state="disabled")

def click_save():
    search_code = set_search()
    user_input = enterSearch.get()
    data = pd.DataFrame([[user_input, search_code]])
    data.to_csv('data.csv', index=False)
    btnRestore.config(fg='green')

def click_restore():
    output.configure(state="normal")
    txt = back.read_saved_search("data.csv")
    output.delete('0.0', tk.END)
    output.insert(tk.END, txt)
    output.configure(state="disabled")

btnSave = tk.Button(root, text="Save", command=click_save)
btnSave.grid(row=3, column=1, padx=1, pady=2)
btnRestore = tk.Button(root, text="Restore", fg="black", command=click_restore)
btnRestore.grid(row=4, column=1, padx=1, pady=2)

def click_track():
    tracking.configure(state="normal")
    flight_num = enterTrack.get()
    try:
        if (flight_num + "\n") in open('track_list.txt', 'r').readlines():
            tracking.configure(state="disabled")
            tkmsg.showinfo("Notice", "Flight " + flight_num + " is already being tracked.")
            return
    except IOError:
        pass
    with open("track_list.txt", 'a+') as track_list:
        track_list.write(flight_num + "\n")
        tkmsg.showinfo("Tracking! ", "Attempting to track " + flight_num)
    tracking.delete('0.0', tk.END)
    tracking.insert(tk.END, back.read_tracking_file())
    tracking.configure(state="disabled")

def click_clear_tracking():
    tracking.configure(state="normal")
    with open("track_list.txt", "w+") as to_clear:
        pass
    tracking.delete('0.0', tk.END)
    tracking.insert(tk.END, "No flights tracked")
    tracking.configure(state="disabled")

def refresh_tracking():
    back.api_response = back.pull_data()
    tracking.configure(state="normal")
    tracking.delete('0.0', tk.END)
    tracking.insert(tk.END, back.read_tracking_file())
    tracking.configure(state="disabled")
    back.send_mail()
    root.after(1000*600, refresh_tracking)

lblTrack = tk.Label(root, text="Enter flight number below to track flights")
lblTrack.grid(row=1, column=2, padx=1, pady=2)
enterTrack = tk.Entry(root, width=20)
enterTrack.grid(row=2, column=2, padx=1, pady=2)
btnTrack = tk.Button(root, text="Track", command=click_track)
btnTrack.grid(row=3, column=3, padx=1, pady=2)
btnClear = tk.Button(root, text="Clear Tracking", command=click_clear_tracking)
btnClear.grid(row=4, column=3, padx=1, pady=2)
tracking = tk.Text(root, height=30, width=40, wrap=tk.WORD)
tracking.grid(row=5, column=2, columnspan=2, padx=1, pady=2)
tracking.insert(tk.END, initial_data)
root.after(1000*600, refresh_tracking)
tracking.config(state="disabled")

root.mainloop()
