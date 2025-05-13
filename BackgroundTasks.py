from threading import *
import json
import time
from Database.DatabaseManager import DataBase
from seasonEndManagement import SeasonEndManagement

class BackgroundTasks(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        db = DataBase(None)
        while True:
            try:
                db.rerollEvents()
            except Exception as e:
                print("[!] Error during event reroll:", e)
            settings = json.load(open('Settings.json'))
            if settings["nextSeasonEndTimestamp"] <= time.time():
                SeasonEndManagement.handleTrophies()
            time.sleep(7)