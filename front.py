import tkinter as tk
import tkinter.messagebox as tkmsg
import pandas as pd
import csv
import back_functions

initial_data = back_functions.start_program()

root = tk.Tk()

root.title("AirTracker V1")
root.geometry('969x750')

menu = tk.Menu(root)
item = tk.Menu(menu)
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

header = tk.Label(root, text="Flight Tracking")
header.grid(row=0, column=1, padx=1, pady=2)

lbl1 = tk.Label(root, text="Search using departure (iata), arrival (iata), airline, or flight number (iata).")
lbl1.grid(row=1, column=1, padx=1, pady=2)

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

search_list = ['Departure (Name)', 'Departure (IATA)', 'Arrival (Name)', 'Arrival (IATA)', 'Airline', 'Flight #']
search_choice = tk.StringVar()
search_choice.set('---')
search_dropdown = tk.OptionMenu(root, search_choice, *search_list)
search_dropdown.grid(row=2, column=1)
enterSearch = tk.Entry(root, width=20)
enterSearch.grid(row=6, column=1, padx=1, pady=2)
output = tk.Text(root, height=20, width=120, wrap=tk.WORD)
output.grid(row=7, column=0, columnspan=3, padx=1, pady=2)

def click_search():
    search_code = set_search()
    user_input = enterSearch.get()
    res = "Searching for " + user_input
    lbl1.configure(text = res)
    output.delete('0.0', tk.END)
    output.insert(tk.END, back_functions.display(user_input, search_code))

btn1 = tk.Button(root, text="Search", fg="red", command=click_search)
btn1.grid(row=6, column=2, padx=1, pady=2)

def click_restore():
    txt = back_functions.read_saved_search("data.csv")
    output.delete('0.0', tk.END)
    output.insert(tk.END, txt)

btnRestore = tk.Button(root, text="Restore", fg="black", command=click_restore)
btnRestore.grid(row=1, column=2, padx=1, pady=2)

def click_save():
    search_code = set_search()
    user_input = enterSearch.get()
    data = pd.DataFrame([[user_input, search_code]])
    data.to_csv('data.csv', index=False)
    btnRestore.config(fg='green')

btnSave = tk.Button(root, text="Save", command=click_save)
btnSave.grid(row=0, column=2, padx=1, pady=2)

def click_track():
    with open("track_list.txt", 'a+') as track_list:
        flight_num = enterTrack.get()
        track_list.write(flight_num + "\n")
        tkmsg.showinfo("Tracking! ", "Now tracking " + flight_num)
    tracking.delete('0.0', tk.END)
    tracking.insert(tk.END, back_functions.read_tracking_file())

def click_clear_tracking():
    with open("track_list.txt", "w+") as to_clear:
        pass
    tracking.delete('0.0', tk.END)
    tracking.insert(tk.END, "No flights tracked")

lbl2 = tk.Label(root, text="Enter flight number below to track flights")
lbl2.grid(row=1, column=0, padx=1, pady=2)
enterTrack = tk.Entry(root, width=20)
enterTrack.grid(row=2, column=0, padx=1, pady=2)
btnTrack = tk.Button(root, text="Track", command=click_track)
btnTrack.grid(row=3, column=0, padx=1, pady=2)
btnClear = tk.Button(root, text="Clear All", command=click_clear_tracking)
btnClear.grid(row=4, column=0, padx=1, pady=2)
tracking = tk.Text(root, height=10, width=120, wrap=tk.WORD)
tracking.grid(row=8, column=0, columnspan=3, padx=1, pady=2)
tracking.insert(tk.END, initial_data)

root.mainloop()
