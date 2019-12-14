# Import required packages
import requests
#import rds_config
import mysql.connector
from datetime import datetime
from datetime import timedelta

db_username = "awesometeam"
db_password = "nandan123"
db_name = "test"
db_endpoint = "big-apple.cbx9jy53wa9n.us-east-2.rds.amazonaws.com"
app_token='x1uqIJMOnjOzlZZUrIcEwUY40'

############################# Calls 311 ###############################
def get_calls_311():
    """Function to connect to the database with information regarding
    the calls to 311 and extract the relevant data.
    """

    #Get API token from file
    # with open("app_token.txt") as file: app_token = file.readline().rstrip()
    #HTTPS address for the APIs
    url_311 = "https://data.cityofnewyork.us/resource/erm2-nwe9.json?"

    #Prepare URL query

    #datetime object containing current date and time
    now = datetime.now()
    last_week = now - timedelta(weeks = 1)

    #Appropriate format for the query
    now_string = now.strftime("%Y-%m-%dT%H:%M:%S")
    last_week_str = last_week.strftime("%Y-%m-%dT%H:%M:%S")

    query_dates_311 = "$where=created_date between " + "'" + last_week_str + "'" + " and " + "'" + now_string + "'" + "&$limit=50000"
    query_311 = url_311 + "$$app_token=" + app_token + "&" + query_dates_311

    #Query the URL and get response
    response = requests.get(query_311)
    calls_311 = response.json()

    #Select keys
    keys_311 = ['unique_key',
                'created_date',
                'closed_date',
                'agency',
                'agency_name',
                'complaint_type',
                'descriptor',
                'incident_zip',
                'borough',
               'facility_type',
               'location_type',
                'status',
               'due_date',
                'resolution_action_updated_date',
                'x_coordinate_state_plane',
                'y_coordinate_state_plane',
                'open_data_channel_type',
                'latitude',
                'longitude']

    #Extract relevant data from the JSON file and store it as a dictionary
    data_311 = []
    for call in calls_311:
        dict_calls = {'unique_key': call['unique_key']}
        for key in keys_311:
           if sum([i==key for i in call.keys()])==1:
               dict_calls[key] = call[key]
           else:
                dict_calls[key] = None
        data_311.append(dict_calls)

    return data_311


def insert_calls_311(data_311):
    """Function to deletes the existing 311 calls table, creates it again,
    and populates it with the data provided as an input.
    """
    #RDS configuration settings
    config = {
      'user': db_username,
      'port': '3306',
      'password': db_password,
      #RDS instace endpoint
      'host': db_endpoint,
      'database': db_name,
      'raise_on_warnings': True
    }
    #MariaDB code for dropping the old table
    drop_311_calls = ("DROP TABLE `311_calls`")
    #MariaDB code for creating the table
    create_311_calls = (
       "CREATE TABLE `311_calls` ("
       "  `unique_key` INTEGER PRIMARY KEY,"
       "  `created_date` VARCHAR(30),"
       "  `closed_date` VARCHAR(30),"
       "  `agency` VARCHAR(30),"
       "  `agency_name` VARCHAR(1000),"
       "  `complaint_type` VARCHAR(1000),"
       "  `descriptor` VARCHAR(1000),"
       " `incident_zip` INTEGER,"
       "  `borough` VARCHAR(30),"
       "  `facility_type` VARCHAR(1000),"
       "  `location_type` VARCHAR(1000),"
       "  `status` VARCHAR(1000),"
       "  `due_date` VARCHAR(30),"
       "  `resolution_action_updated_date` VARCHAR(30),"
       "  `x_coordinate_state_plane` INTEGER,"
       "  `y_coordinate_state_plane` INTEGER,"
       "  `open_data_channel_type` VARCHAR(30),"
       "  `latitude` VARCHAR(30),"
       " `longitude` VARCHAR(30)"
       ") ENGINE=InnoDB")

    #Query to insert data into MariaDB
    calls_sql = (
       "insert into 311_calls"
       "(unique_key, created_date, closed_date, agency, agency_name, complaint_type,"
                "descriptor, location_type, incident_zip, borough, facility_type,"
                "status, due_date, resolution_action_updated_date, x_coordinate_state_plane,"
                "y_coordinate_state_plane, open_data_channel_type, latitude, longitude)"
       "values (%(unique_key)s, %(created_date)s, %(closed_date)s, %(agency)s, %(agency_name)s, %(complaint_type)s,"
                "%(descriptor)s, %(location_type)s, %(incident_zip)s, %(borough)s, %(facility_type)s,"
                "%(status)s, %(due_date)s, %(resolution_action_updated_date)s, %(x_coordinate_state_plane)s,"
                "%(y_coordinate_state_plane)s, %(open_data_channel_type)s, %(latitude)s, %(longitude)s)")

    #Setup the connector
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    #Drop the table and generate it again
    try:
        cursor.execute(drop_311_calls)
    except:
        print('Table does not exist')

    cursor.execute(create_311_calls)
    #Insert the data into the database
    for call in data_311:
       cursor.execute(calls_sql, call)
    #Commit changes and close cursor
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Done. Calls 311 data introduced in the database')
############################# Events ###############################
def get_events():
    """Function to connect to the database with information regarding
    the events in New York and extract the relevant data.
    """
    #Get API token from file
    # with open("app_token.txt") as file: app_token = file.readline().rstrip()

    # HTTPS address for the APIs
    url_events = "https://data.cityofnewyork.us/resource/tvpp-9vvx.json?"

    # Prepare URL query

    #datetime object containing current date and time
    now = datetime.now()
    last_week = now - timedelta(weeks = 1)

    #Appropriate format for the query
    now_string = now.strftime("%Y-%m-%dT%H:%M:%S")
    last_week_str = last_week.strftime("%Y-%m-%dT%H:%M:%S")

    #TO DO: make the query dates a parameter of the function
    query_events = "$where=start_date_time between " + "'" + last_week_str + "' and '"  + now_string + "'" + "&$limit=50000"
    query_url_events = url_events + "$$app_token=" + app_token + "&" + query_events

    #Query the URL and get response
    response = requests.get(query_url_events)
    events = response.json()

    #Select keys
    keys_events = ['event_id', 'event_name', 'start_date_time', 'end_date_time',
                   'event_agency', 'event_type', 'event_borough', 'event_location']

    #Extract relevant data from the JSON file and store it as a dictionary
    data_events = []
    for a in events:
        #start by adding the event_id to the dictionary
        dict_events = {'event_id': a['event_id']}
        for key in keys_events:
           if sum([k == key for k in a.keys()])== 1:
               dict_events[key] = a[key]
           else:
                dict_events[key] = None
        data_events.append(dict_events)

    return data_events
def insert_events(data_events):
    """Function to deletes the existing events table, creates it again,
    and populates it with the data provided as an input.
    """
    #RDS configuration settings
    config = {
      'user': db_username,
      'port': '3306',
      'password': db_password,
      #RDS instace endpoint
      'host': db_endpoint,
      'database': db_name,
      'raise_on_warnings': True
    }

    #MariaDB code to drop table
    drop_events = ("DROP TABLE `events`")

    #MariaDB code to create table
    create_events = (
       "CREATE TABLE `events` ("
       "  `event_id` int(10) NOT NULL,"
       "  `event_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,"
       "  `start_date_time` datetime NOT NULL,"
       "  `end_date_time` datetime NOT NULL,"
       "  `event_agency` varchar(255),"
       "  `event_type` varchar(255),"
       "  `event_borough` varchar(255),"
       " `event_location` varchar (500),"
       "  PRIMARY KEY (`event_id`,`start_date_time`)"
       ") ENGINE=InnoDB")

    #Query to insert data into MariaDB
    events_sql = (
       "insert into events"
       "(event_id, event_name, start_date_time, end_date_time,"
        "event_agency, event_type, event_borough, event_location)"

        "values (%(event_id)s, %(event_name)s, %(start_date_time)s, %(end_date_time)s, %(event_agency)s, %(event_type)s,"
        "%(event_borough)s, %(event_location)s)")

    #Setup the connector
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    #Drop table and regenerate it
    try:
        cursor.execute(drop_events)
    except:
        print('Table does not exist')

    cursor.execute(create_events)

    #Insert the data into the database
    for event in data_events:
        cursor.execute(events_sql, event)

    #Commit changes and close the cursor
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Done. Events data introduced in the database')

############################# DHS ###############################
def get_dhs():
    """Function to connect to the database with information regarding
    the information from the DHS and extract the relevant data.
    """
    #Get API token from file
    # with open("app_token.txt") as file: app_token = file.readline().rstrip()

    # HTTPS address for the APIs
    url_dhs = "https://data.cityofnewyork.us/resource/k46n-sa2m.json?"

    # Prepare URL query

    #datetime object containing current date and time
    now = datetime.now()
    last_week = now - timedelta(weeks = 1)

    #Appropriate format for the query
    now_string = now.strftime("%Y-%m-%dT%H:%M:%S")
    last_week_str = last_week.strftime("%Y-%m-%dT%H:%M:%S")

    #TO DO: make the query dates a parameter of the function
    query_dates_dhs = "$where=date_of_census between " + "'" + last_week_str + "' and '"  + now_string + "'" + "&$limit=1000"
    query_dhs = url_dhs + "$$app_token=" + app_token + "&" + query_dates_dhs

    #Query the URL and get response
    response = requests.get(query_dhs)
    dhs = response.json()

    #Select keys
    keys_dhs = ['date_of_census',
                 'total_adults_in_shelter',
                 'total_children_in_shelter',
                 'total_individuals_in_shelter',
                 'single_adult_men_in_shelter',
                 'single_adult_women_in_shelter',
                 'total_single_adults_in_shelter',
                 'families_with_children_in_shelter',
                 'adults_in_families_with_children_in_shelter',
                 'children_in_families_with_children_in_shelter',
                 'total_individuals_in_families_with_children_in_shelter_',
                 'adult_families_in_shelter',
                 'individuals_in_adult_families_in_shelter']

    #Extract relevant data from the JSON file and store it as a dictionary
    data_dhs = []
    for record in dhs:
        dict_dhs = {'date_of_census': record['date_of_census']}
        for key in keys_dhs:
           if sum([i==key for i in record.keys()])==1:
               dict_dhs[key] = record[key]
           else:
                dict_dhs[key] = None
        data_dhs.append(dict_dhs)

    return data_dhs
def insert_dhs(data_dhs):
    """Function to deletes the existing DHS table, creates it again,
    and populates it with the data provided as an input.
    """
    #RDS configuration settings
    config = {
      'user': db_username,
      'port': '3306',
      'password': db_password,
      #RDS instace endpoint
      'host': db_endpoint,
      'database': db_name,
      'raise_on_warnings': True
    }

    #MariaDB code to delete table and create it again
    drop_dhs = ("DROP TABLE `dhs`")
    create_dhs = (
       "CREATE TABLE `dhs` ("
       "  `date_of_census` VARCHAR(30) PRIMARY KEY,"
       "  `total_adults_in_shelter` INTEGER,"
       "  `total_children_in_shelter` INTEGER,"
       "  `total_individuals_in_shelter` INTEGER,"
       "  `single_adult_men_in_shelter` INTEGER,"
       "  `single_adult_women_in_shelter` INTEGER,"
       "  `total_single_adults_in_shelter` INTEGER,"
       "  `families_with_children_in_shelter` INTEGER,"
       "  `adults_in_families_with_children_in_shelter` INTEGER,"
       "  `children_in_families_with_children_in_shelter` INTEGER,"
       "  `total_individuals_in_families_with_children_in_shelter_` INTEGER,"
       "  `adult_families_in_shelter` INTEGER,"
       "  `individuals_in_adult_families_in_shelter` INTEGER"
       ") ENGINE=InnoDB")

    #Query to insert data into MariaDB
    dhs_sql = ("insert into dhs"
           "(date_of_census, total_adults_in_shelter, total_children_in_shelter, total_individuals_in_shelter,"
                    "single_adult_men_in_shelter, single_adult_women_in_shelter, total_single_adults_in_shelter,"
                    "families_with_children_in_shelter, adults_in_families_with_children_in_shelter,"
                    "children_in_families_with_children_in_shelter, total_individuals_in_families_with_children_in_shelter_,"
                    "adult_families_in_shelter, individuals_in_adult_families_in_shelter)"
           "values (%(date_of_census)s, %(total_adults_in_shelter)s, %(total_children_in_shelter)s, %(total_individuals_in_shelter)s,"
                    "%(single_adult_men_in_shelter)s, %(single_adult_women_in_shelter)s, %(total_single_adults_in_shelter)s,"
                    "%(families_with_children_in_shelter)s, %(adults_in_families_with_children_in_shelter)s,"
                    "%(children_in_families_with_children_in_shelter)s, %(total_individuals_in_families_with_children_in_shelter_)s,"
                    "%(adult_families_in_shelter)s, %(individuals_in_adult_families_in_shelter)s)")

    #Setup the connector
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    #Delete the table and regenerate it
    try:
        cursor.execute(drop_dhs)
    except:
        print('Table does not exist')
    cursor.execute(create_dhs)

    #Insert the data into the database
    for day in data_dhs:
       cursor.execute(dhs_sql, day)

    #Commit changes and close cursor
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Done. DHS data introduced in the database')

############################# Accidents ###############################
def get_accidents():
    """Function to connect to the database with information regarding
    the accidents in New York and extract the relevant data.
    """
    #Get API token from file
    # with open("app_token.txt") as file: app_token = file.readline().rstrip()

    # HTTPS address for the APIs
    url_acc = "https://data.cityofnewyork.us/resource/h9gi-nx95.json?"

    # Prepare URL query

    #datetime object containing current date and time
    now = datetime.now()
    last_week = now - timedelta(weeks = 1)

    #Appropriate format for the query
    now_string = now.strftime("%Y-%m-%dT%H:%M:%S")
    last_week_str = last_week.strftime("%Y-%m-%dT%H:%M:%S")

    #TO DO: make the query dates a parameter of the function
    query_acc = "$where=crash_date between " + "'" + last_week_str + "' and '"  + now_string + "'" + "&$limit=50000"
    query_url_acc = url_acc + "$$app_token=" + app_token + "&" + query_acc


    #Query the URL and get response
    response = requests.get(query_url_acc)
    acc = response.json()

    #Select keys
    keys_acc =  ["collision_id", "crash_date", "crash_time",
                 "borough", "zip_code", "latitude", "longitude",
                 "number_of_persons_injured", "number_of_persons_killed",
                 "number_of_pedestrians_injured", "number_of_pedestrians_killed",
                 "number_of_cyclist_injured", "number_of_cyclist_killed",
                 "number_of_motorist_injured", "number_of_motorist_killed",
                 "contributing_factor_vehicle_1", "contributing_factor_vehicle_2"]

    #Extract relevant data from the JSON file and store it as a dictionary
    data_acc = []
    for a in acc:
        #start by adding the collission_id to the dictionary
        dict_acc = {'collision_id': a['collision_id']}
        for key in keys_acc:
           if sum([k == key for k in a.keys()])== 1:
               dict_acc[key] = a[key]
           else:
                dict_acc[key] = None
        data_acc.append(dict_acc)

    return data_acc

def insert_accidents(data_acc):
    """Function to deletes the existing accidents table, creates it again,
    and populates it with the data provided as an input.
    """
    #RDS configuration settings
    config = {
      'user': db_username,
      'port': '3306',
      'password': db_password,
      #RDS instace endpoint
      'host': db_endpoint,
      'database': db_name,
      'raise_on_warnings': True
    }

    #MariaDB code to delete the table and re create it
    drop_accidents = ("DROP TABLE `accidents`")
    create_accidents = (
        "CREATE TABLE `accidents` ("
        "  `collision_id` INTEGER PRIMARY KEY,"
        "  `crash_date` DATETIME,"
        "  `crash_time` TIME,"
        "  `borough` VARCHAR(30),"
        "  `zip_code` INTEGER,"
        "  `latitude` INTEGER,"
        "  `longitude` INTEGER,"
        "  `number_of_persons_injured` INTEGER,"
        "  `number_of_persons_killed` INTEGER,"
        "  `number_of_pedestrians_injured` INTEGER,"
        "  `number_of_pedestrians_killed` INTEGER,"
        "  `number_of_cyclist_injured` INTEGER,"
        "  `number_of_cyclist_killed` INTEGER,"
        "  `number_of_motorist_injured` INTEGER,"
        "  `number_of_motorist_killed` INTEGER,"
        "  `contributing_factor_vehicle_1` VARCHAR(1000),"
        "  `contributing_factor_vehicle_2` VARCHAR(1000)"
        ") ENGINE=InnoDB")

    #Query to insert data into MariaDB
    acc_sql = (
       "insert into accidents"
       "(collision_id, crash_date, crash_time, borough, zip_code, latitude, longitude,"
        "number_of_persons_injured, number_of_persons_killed, "
        "number_of_pedestrians_injured, number_of_pedestrians_killed, "
        "number_of_cyclist_injured, number_of_cyclist_killed, "
        "number_of_motorist_injured, number_of_motorist_killed, "
        "contributing_factor_vehicle_1, contributing_factor_vehicle_2)"

        "values (%(collision_id)s, %(crash_date)s, %(crash_time)s, %(borough)s, %(zip_code)s, %(latitude)s,"
        "%(longitude)s, %(number_of_persons_injured)s, %(number_of_persons_killed)s,"
        "%(number_of_pedestrians_injured)s, %(number_of_pedestrians_killed)s, %(number_of_cyclist_injured)s,"
        "%(number_of_cyclist_killed)s, %(number_of_motorist_injured)s, %(number_of_motorist_killed)s,"
        "%(contributing_factor_vehicle_1)s, %(contributing_factor_vehicle_2)s)")


    #Setup the connector
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    #Delete table and re create it
    try:
        cursor.execute(drop_accidents)
    except:
        print('Table does not exist')
    cursor.execute(create_accidents)

    #Insert the data into the database
    for acc in data_acc:
        cursor.execute(acc_sql, acc)

    #Commmit the changes and close the connection
    cnx.commit()
    cursor.close()
    cnx.close()

    print('Done. Accidents data introduced in the database')

###################### FUNCTION EXECUTION ##############################

# #311 Calls
# data_311 = get_calls_311()
# insert_calls_311(data_311)

# #Events
# events = get_events()
# insert_events(events)

# #DHS
# dhs = get_dhs()
# insert_dhs(dhs)

# #Accidents
# accidents = get_accidents()
# insert_accidents(accidents)

def lambda_handler(event, context):
    # TODO implement

    #311 Calls
    data_311 = get_calls_311()
    insert_calls_311(data_311)

    #Events
    events = get_events()
    insert_events(events)

    #DHS
    dhs = get_dhs()
    insert_dhs(dhs)

    #Accidents
    accidents = get_accidents()
    insert_accidents(accidents)

    return {
        'statusCode': 200,
        'body': 'Load complete! With timer!'
    }
