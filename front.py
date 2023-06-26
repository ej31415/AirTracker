import tkinter as tk
import pandas as pd
import csv
import back_functions

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

enter = tk.Entry(root, width=20)
enter.grid(row=6, column=1, padx=1, pady=2)

output = tk.Text(root, height=20, width=120, wrap=tk.WORD)
output.grid(row=7, column=0, columnspan=3, padx=1, pady=2)

def click_search():
    search_code = set_search()
    user_input = enter.get()
    res = "Searching for " + user_input
    lbl1.configure(text = res)
    output.delete('0.0', tk.END)
    output.insert(tk.END, back_functions.display(user_input, search_code))

btn1 = tk.Button(root, text="Search", fg="red", command=click_search)
btn1.grid(row=6, column=2, padx=1, pady=2)

def click_restore():
    with open("data.csv") as data_file:
        reader = csv.reader(data_file)
        for row in reader:
            term = row[0]
            code = int(row[1])
        output.delete('0.0', tk.END)
        output.insert(tk.END, back_functions.display(term, code))

btnRestore = tk.Button(root, text="Restore", fg="black", command=click_restore)
btnRestore.grid(row=1, column=2, padx=1, pady=2)

def click_save():
    search_code = set_search()
    user_input = enter.get()
    data = pd.DataFrame([[user_input, search_code]])
    data.to_csv('data.csv', index=False)
    btnRestore.config(fg='green')

btnSave = tk.Button(root, text="Save", command=click_save)
btnSave.grid(row=0, column=2, padx=1, pady=2)

root.mainloop()
