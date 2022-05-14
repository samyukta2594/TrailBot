# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.types import DomainDict
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet
import sqlite3
import random
from pathlib import Path
import http.client


import requests

ALLOWED_TRAIL_DIFFICULTIES = ["Easy", "Moderate", "Hard"]
ALLOWED_TRAIL_PLACES = ["Cupertino", "Sunnyvale", "Campbell", "Milpitas", "Saratoga", "Fremont"]


class ValidateSimpleTrailForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_trail_form"

    def validate_difficulty(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `trail_difficulty` value."""

        if slot_value not in ALLOWED_TRAIL_DIFFICULTIES:
            dispatcher.utter_message(text=f"We only accept follwing trails: Easy/Moderate/Hard.")
            return {"difficulty": None}
        dispatcher.utter_message(text=f"You want to have a {slot_value} hike.")
        return {"difficulty": slot_value}

    def validate_place(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `trail_place` value."""

        if slot_value not in ALLOWED_TRAIL_PLACES:
            dispatcher.utter_message(text=f"I don't recognize that place. We serve {'/'.join(ALLOWED_TRAIL_PLACES)}.")
            return {"place": None}
        dispatcher.utter_message(text=f"Awesome! You want hike in {slot_value}")
        return {"place": slot_value}

class ValidateSimpleScheduleForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_schedule_form"

    def validate_user_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `user_name` value."""
        print("user_name")
        print(slot_value)
        return {"user_name": slot_value}

    def validate_user_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `user_email` value."""

        print("email")
        print(slot_value)
        return {"user_email": slot_value}

    def validate_trail_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `trail_name` value."""

        print("trail_name")
        print(slot_value)
        return {"trail_name": slot_value}

class ActionMoreInformation(Action):

    def name(self) -> Text:
        return "action_more_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            try:
                from googlesearch import search
            except ImportError:
                print("No module named 'google' found")
            # to search
            query = tracker.get_slot("trail_name")

            msg = "You can find more information here :"
            link = ""
            for j in search(query, tld="co.in", num=1, stop=1, pause=2):
                msg += j
                link = j
            


            dispatcher.utter_message(text=msg)
            
            return [SlotSet("link",link)]

class ActionGetWeather(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        city = tracker.get_slot("place")
        if not city:
            dispatcher.utter_message(text=f"I don't recognize that place. Please enter from {'/'.join(ALLOWED_TRAIL_PLACES)}.")
            return [SlotSet("place", None)]

        # Call weather API
        api_key = '7f5a01b293defd5979a61f46f548bccd'
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
        response = requests.get(url)
        json = response.json()

        if json["cod"] != 200 :
            dispatcher.utter_message(text="Invalid city")
            return [SlotSet("place", None)]
        
        #Extract required details
        city = json["name"]
        weather_main = json["weather"][0]["main"]
        weather_desc = json["weather"][0]["description"]
        temperature = json["main"]["temp"]
        temp_min = json["main"]["temp_min"]
        temp_max = json["main"]["temp_max"]

        text = f"The weather in {city} : {weather_main}, {weather_desc} \n Temperature (F) : {temperature}  Min: {temp_min}  Max: {temp_max}"
        dispatcher.utter_message(text=text)

        return []


class ActionGetHumidity(Action):

    def name(self) -> Text:
        return "action_get_humidity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        city = tracker.get_slot("place")
        if not city:
            dispatcher.utter_message(text=f"I don't recognize that place. Please enter from {'/'.join(ALLOWED_TRAIL_PLACES)}.")
            return [SlotSet("place", None)]

        # Call weather API
        api_key = '7f5a01b293defd5979a61f46f548bccd'
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
        response = requests.get(url)
        json = response.json()

        if json["cod"] != 200 :
            dispatcher.utter_message(text="Invalid city")
            return [SlotSet("place", None)]
        
        #Extract required details
        city = json["name"]
        humidity = json["main"]["humidity"]


        text = f"The humidity level in {city} is {humidity}"
        dispatcher.utter_message(text=text)

        return []

class ActionGetFact(Action):

    def name(self) -> Text:
        return "action_get_fact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        limit = 1
        api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
        response = requests.get(api_url, headers={'X-Api-Key': 'W0HcbiGniznn5xptoSKCNQ==Uh8q5B5CReBlGMGB'})
        if response.status_code == requests.codes.ok:
            data = response.json()
            print(data[0]['fact'])
            dispatcher.utter_message(text=data[0]['fact'])
        else:
            print("Error:", response.status_code, response.text)
            dispatcher.utter_message(text="Server error. Please try again later.")

        return []

class ActionCheckDogFriendly(Action):

    def name(self) -> Text:
        return "action_check_dog_friendly"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        dog_friendly = tracker.get_slot("dog_friendly")
        if dog_friendly:
            dispatcher.utter_message(text="Yes. It is a dog friendly trail.")
        else:
            dispatcher.utter_message(text="No")

        return []

class ActionCheckWheelchair(Action):

    def name(self) -> Text:
        return "action_check_wheelchair"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        wheelchair = tracker.get_slot("wheelchair")
        if wheelchair:
            dispatcher.utter_message(text="Yes. It is a wheel chair friendly trail.")
        else:
            dispatcher.utter_message(text="No")

        return []

class ActionCheckParking(Action):

    def name(self) -> Text:
        return "action_check_parking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        parking = tracker.get_slot("parking")
        if int(parking) is not 0:
            dispatcher.utter_message(text=f"You have to pay USD {parking}")
        else:
            dispatcher.utter_message(text="Parking is free")

        return []

class ActionCheckElevation(Action):

    def name(self) -> Text:
        return "action_check_elevation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        elevation = tracker.get_slot("elevation")

        dispatcher.utter_message(text=f"The elevation gain is {elevation} ft")

        return []

class ActionCheckLength(Action):

    def name(self) -> Text:
        return "action_check_length"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Check city validity
        length = tracker.get_slot("length")

        dispatcher.utter_message(text=f"The length of the loop is {length} miles")

        return []


class QueryResourceType(Action):

    def name(self) -> Text:
        return "query_resource_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fpath = Path('db_data/trail_DB').absolute()
        print(fpath)
        conn = create_connection(fpath)

        slot_value = next(tracker.get_latest_entity_values("place",None))
        print(slot_value)
        slot_name = "Place"
        get_query_results = select_by_slot(conn, slot_name,slot_value)
        msg = "You can try out the " + str(get_query_results)
        print(msg)
        if not slot_value:
            dispatcher.utter_message(text="No slot returned")
            return []
        else:
            dispatcher.utter_message(text=msg)
            return []
        return []

class QueryTrailChoice(Action):

    def name(self) -> Text:
        return "query_trail_choice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fpath = Path('db_data/trail_DB').absolute()
        print(fpath)
        conn = create_connection(fpath)

        slot_value_place = tracker.get_slot("place")
        slot_value_diffculty = tracker.get_slot("difficulty")
        print(slot_value_place)
        print(slot_value_diffculty)
        
        slot_name_place = "Place"
        slot_name_difficulty = "Difficulty "
        get_query_results = select_trails(conn, slot_name_place,slot_value_place,slot_name_difficulty,slot_value_diffculty)
        print(get_query_results)
        print(type(get_query_results))
        print(get_query_results[0][3])
        msg = "You can try out the " + get_query_results[0][0] + " at " + get_query_results[0][1]
        trail_name = get_query_results[0][0]
        dog_friendly = get_query_results[0][7]
        wheelchair = get_query_results[0][6]
        elevation = get_query_results[0][5]
        parking = get_query_results[0][8]
        length = get_query_results[0][3]
        if not get_query_results:
            dispatcher.utter_message(text="No slot returned")
            return []
        else:
            dispatcher.utter_message(text=msg)
            return [SlotSet("trail_name", trail_name), SlotSet("dog_friendly",dog_friendly), SlotSet("elevation",elevation),SlotSet("wheelchair",wheelchair),SlotSet("parking",parking),SlotSet("length",length)]
        return []

class ScheduleTrailChoice(Action):

    def name(self) -> Text:
        return "schedule_trail_choice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        fpath = Path('db_data/trail_DB').absolute()
        conn = create_connection(fpath)

        slot_value_user_name = tracker.get_slot("user_name")
        slot_value_user_email = tracker.get_slot("user_email")
        slot_value_trail_name = tracker.get_slot("trail_name")
        slot_value_place = tracker.get_slot("place")

        get_query_results = insert_schedule_toDB(conn,slot_value_user_name,slot_value_user_email,slot_value_trail_name,slot_value_place)

        if not get_query_results:
            dispatcher.utter_message(text="Error saving schedule")
            return []
        else:
            dispatcher.utter_message(text="Schedule saved. You can continue looking for other trails.")
            return [AllSlotsReset()]
        return []

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def insert_schedule_toDB(conn,slot_value_user_name,slot_value_user_email,slot_value_trail_name,slot_value_place):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """

    try:
        cur = conn.cursor()
        cur.execute(f"""INSERT into user_trail_schedule(UserName,Email,TrailName,Location)
        values ("{slot_value_user_name}","{slot_value_user_email}","{slot_value_trail_name}","{slot_value_place}")
        """)

        conn.commit()
        return 1
    except Exception as e:
        print(e)

def select_trails(conn,slot_name_place,slot_value_place,slot_name_difficulty,slot_value_diffculty):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM trails
    where {slot_name_place} = "{slot_value_place}" and  {slot_name_difficulty} = "{slot_value_diffculty}"
    """)

    rows = cur.fetchall()

    if len(list(rows)) < 1:
        return[("There are no resources matching your query")]
    else:
        for row in random.sample(rows,1):
            return[(row)]

def select_by_slot(conn,slot_name, slot_value):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM trails
    where {slot_name} = "{slot_value}"
    """)

    rows = cur.fetchall()

    if len(list(rows)) < 1:
        return[("There are no resources matching your query")]
    else:
        for row in random.sample(rows,1):
            return[(row[0])]