import csv
import smtplib
import email.message as em
import config


# # For actual use (limited 100 requests per month)
# import requests

# def pull_data():
#     params = {
#     'access_key': config.access_key
#     }

#     api_result = requests.get('http://api.aviationstack.com/v1/flights', params)
#     return api_result.json()

# api_response = pull_data()


# For testing features
import sample_data_set

def pull_data():
    return sample_data_set.get_data()

api_response = sample_data_set.get_data()


def start_program():
    """
    All the things that happen in the back when the program starts
    """
    track_data = ""
    try:
        track_data = read_tracking_file()
    except IOError:
        track_data += "No flights tracked"
    return track_data

def display(term, group):
    """
    Get display text based on the search term

    Input   --  String term representing user input
                Integer group representing what type of input is entered
    
    Output  --  String txt is the display text
    """
    txt = ""
    found = False

    for flight in api_response['data']:
        if group == 1:
            check = flight['departure']['airport']
        elif group == 2:
            check = flight['departure']['iata']
        elif group == 3:
            check = flight['arrival']['airport']
        elif group == 4:
            check = flight['arrival']['iata']
        elif group == 5:
            check = flight['airline']['name']
        elif group == 6:
            check = flight['flight']['iata']
        else:
            return "Please select an option."

        if (check == term):
            found = True
            txt += (u'%s flight %s: %s (%s) to %s (%s) \n' % (
                flight['airline']['name'],
                flight['flight']['iata'],
                flight['departure']['airport'],
                flight['departure']['iata'],
                flight['arrival']['airport'],
                flight['arrival']['iata']))
            depart_time = flight['departure']['scheduled']
            arrival_time = flight['arrival']['scheduled']
            txt += 'Departing at ' + depart_time[depart_time.index("T")+1:depart_time.index("T")+9]
            if flight['departure']['delay'] == None:
                txt += ' (on time) '
            else:
                txt += ' (delayed ' + str(flight['departure']['delay']) + ' minutes) '
            txt += '--> Arrival at ' + arrival_time[arrival_time.index("T")+1:arrival_time.index("T")+9]
            if flight['arrival']['delay'] == None:
                txt += ' (on time)\n\n'
            else:
                txt += ' (delayed ' + str(flight['arrival']['delay']) + ' minutes)\n\n'
    
    if not found:
        txt = "Sorry, none matching \"" + term + "\" is found. \nPlease check for spelling, casing, etc.\n\n"
    
    return txt

def read_saved_search(file_name):
    """
    Read searches saved in the .csv file

    Input   --  String file_name is the name of the save file (always "data.csv")

    Output  --  String txt for the display text
    """
    try:
        with open(file_name) as data_file:
            txt = ""
            reader = csv.reader(data_file)
            next(reader, None)
            for row in reader:
                term = row[0]
                code = int(row[1])
                txt += display(term, code)
            return txt
    except IOError:
        return "No saved searches."

def read_search_list(track_list):
    """
    Get data for a list of flight numbers

    Input   --  track_list is a list of flight numbers (IATA)

    Output  --  txt is a String of each flight's data from track_list
    """
    txt = ""
    for term in track_list:
        txt += display(term[:-1], 6)
    return txt

def read_tracking_file():
    """
    Read "track_list.txt" to produce the output for all the flights tracked
    """
    track_list = open('track_list.txt', 'r').readlines()
    track_data = read_search_list(track_list)
    if track_data == "":
        track_data += "No flights tracked"
    return track_data

def get_data_list(group):
    choices = set([])
    for flight in api_response['data']:
        addition = ''
        if group == 1:
            addition = flight['departure']['airport']
        elif group == 2:
            addition = flight['departure']['iata']
        elif group == 3:
            addition = flight['arrival']['airport']
        elif group == 4:
            addition = flight['arrival']['iata']
        elif group == 5:
            addition = flight['airline']['name']
        elif group == 6:
            addition = flight['flight']['iata']
        if addition != None:
            choices.add(addition)
    return sorted(choices)

def send_mail():
    EMAIL_ADDRESS = config.EMAIL_ADDRESS
    EMAIL_PASSWORD = config.EMAIL_PASSWORD
    
    msg = em.EmailMessage()
    msg['Subject'] = 'Testing Subject'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'xiaodongxie04@gmail.com'
    msg.set_content('Hi')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
        smtp.send_message(msg)

