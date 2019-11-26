# -*- coding: utf-8 -*-
"""Models

This module stores advanced objects used in the app.
"""
from pyttsx3 import init as tts_init
from random import choice
from sched import Event
from sched import scheduler
from string import ascii_lowercase
from time import sleep
from time import time
from threading import Thread

# Type hinting
from datetime import datetime
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
    
from config import Config

RANDOM_DEPTH = 10
TTS_MESSAGE = Config.TTS_MESSAGE

class AlarmManager(scheduler):
    """Extension class of the base scheduler to make alarms management simple.

    Attributes:
        pending_alarms (List of Alarms) &
        finished_alarms (List of Alarms):
            Each storing alarms as dictionaries with keys:
            alarm = {
                "name": (str),
                "string_time": (str),
                "datetime": datetime,
                "alarm_id": (str),
                "event": (Event)
            }
        tts (Pyttsx3 Engine): An object responsible for relaying text to speach
            messages.

    Methods:
    """
    def __init__(self) -> None:
        """Initiates superclass, text to speach, and declares attributes.
        """
        scheduler.__init__(self, time, sleep)
        self.pending_alarms = []
        self.finished_alarms = []
        # Text to speach
        self.tts = tts_init()
        self.tts.setProperty("rate", 130)
        Thread(target=self.tts.startLoop).start()

    @staticmethod # This method is arbitrary.
    def generate_string_id() -> str:
        """Creates a genuinely random set of unique characters unlikely to be
        used twice.
        """
        return "".join(choice(ascii_lowercase) for x in range(RANDOM_DEPTH))

    def create_alarm(self, name: str, datetime: datetime) -> None:
        """Registers a new alarm and adds it to the list of pending alarms.

        Args:
            name (str): Alarm's display name.
            datetime (datetime): Alarm's designated time.
        """
        alarm_id = self.generate_string_id()
        string_time = datetime.strftime("%H:%M %d %B %Y")
        event = self.enterabs(datetime.timestamp(),
                              1,
                              self.trigger_alarm,
                              argument=(alarm_id,))
        if len(self.queue) == 1: # If this new event is the only event,
                                 # the scheduler was not running and needs to.
            self.run()

        new_alarm = {
            "name": name,
            "string_time": string_time,
            "datetime": datetime,
            "alarm_id": alarm_id,
            "event": event,
        }
        print("Adding alarm")
        # Add the new alarm in time sorted position.
        # Beginning from the soonest alarm, and going to the latest -
        for x in range(len(self.pending_alarms)):
            alarm = self.pending_alarms[x]
            # - If this is the first alarm is set to go off after new one -
            if alarm.datetime > new_alarm.datetime:
                # - Then this is the correct position.
                self.pending_alarms.insert(x, new_alarm)
                return
        # The table was either empty, or this is the longest alarm so it goes
        # at the end.
        self.pending_alarms.append(new_alarm)

    def trigger_alarm(self, alarm_id: str) -> None:
        """An alarm has ended, and will be moved from pending to finished.
        The alarm will also be broadcast on text to speach.
        
        Args:
            alarm_id (str): The id for the alarm that has finished.
        """
        alarm = self.remove_alarm_from_list(self.pending_alarms, alarm_id)

        self.tts.say(TTS_MESSAGE % alarm.name)

        self.finished_alarms.insert(0, alarm)

    def remove_pending_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Takes an alarm out of the pending alarms.
        
        Args:
            alarm_id (str): The id for the alarm to remove.

        Returns:
            The alarm, a dictionary.
        """
        alarm = self.remove_alarm_from_list(self.pending_alarms, alarm_id)
        if alarm:
            self.cancel(alarm.event)
            return alarm

    def remove_finished_alarm(self, alarm_id: str) -> Dict[str, Any]:
        """Takes an alarm out of the finished alarms.

        Args:
            alarm_id (str): The id for the alarm to remove.

        Returns:
            The alarm, a dictionary.
        """
        return remove_alarm_from_list(self.finished_alarms, alarm_id)

    def remove_alarm_from_list(self, 
                               list: List[Dict],
                               alarm_id: str) -> Dict[str, Any]:
        """Takes an alarm out of a list of alarms.

        Args:
            alarm_id (str): The id for the alarm to remove.

        Returns:
            The alarm, a dictionary.
        """
        for alarm in list:
            if alarm["alarm_id"] == alarm_id:
                list.remove(alarm)
                return alarm

    def run(self, blocking: bool = True) -> None:
        """Runs the superclass run on a thread so it doesn't stop the entire
        sodding program, like who thought people would appreciate that.
        """
        Thread(target=scheduler.run, args=(self,)).start()
