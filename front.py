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
# header.pack()
header.grid(row=0, column=1, padx=1, pady=2)

lbl1 = tk.Label(root, text="Search using departure (iata), arrival (iata), airline, or flight number (iata).")
# lbl1.pack()
lbl1.grid(row=1, column=1, padx=1, pady=2)

search_code = 0
def set_search():
    if button_dep_state.get() == 1:
        return 1
    elif button_arr_state.get() == 1:
        return 2
    elif button_air_state.get() == 1:
        return 3
    elif button_fli_state.get() == 1:
        return 4

def check1():
    button_search_arr.deselect()
    button_search_air.deselect()
    button_search_fli.deselect()

def check2():
    button_search_dep.deselect()
    button_search_air.deselect()
    button_search_fli.deselect()

def check3():
    button_search_dep.deselect()
    button_search_arr.deselect()
    button_search_fli.deselect()

def check4():
    button_search_dep.deselect()
    button_search_arr.deselect()
    button_search_air.deselect()

button_dep_state = tk.IntVar()
button_arr_state = tk.IntVar()
button_air_state = tk.IntVar()
button_fli_state = tk.IntVar()
button_search_dep = tk.Checkbutton(root, text="Departure", variable=button_dep_state, command=check1)
button_search_arr = tk.Checkbutton(root, text="Arrival", variable=button_arr_state, command=check2)
button_search_air = tk.Checkbutton(root, text="Airline", variable=button_air_state, command=check3)
button_search_fli = tk.Checkbutton(root, text="Flight #", variable=button_fli_state, command=check4)
# button_search_dep.pack()
# button_search_arr.pack()
# button_search_air.pack()
# button_search_fli.pack()
button_search_dep.grid(row=2, column=1)
button_search_arr.grid(row=3, column=1)
button_search_air.grid(row=4, column=1)
button_search_fli.grid(row=5, column=1)

enter = tk.Entry(root, width=20)
# enter.pack()
enter.grid(row=6, column=1, padx=1, pady=2)

output = tk.Text(root, height=20, width=120, wrap=tk.WORD)
# output.pack()
output.grid(row=7, column=0, columnspan=3, padx=1, pady=2)

def click_search():
    search_code = set_search()
    user_input = enter.get()
    res = "Searching for " + user_input
    lbl1.configure(text = res)
    output.delete('0.0', tk.END)
    output.insert(tk.END, back_functions.display(user_input, search_code))

btn1 = tk.Button(root, text="Search", fg="red", command=click_search)
# btn1.pack()
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
