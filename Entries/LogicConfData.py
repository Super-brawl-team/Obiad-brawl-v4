from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
from Logic.Milestones import Milestones
import json
import random
from time import *
from Files.CsvLogic.Locations import Locations

class LogicConfData:
    def encode(self: Writer, player):
        db = DataBase(player)
        self.player = player
        self.settings = json.load(open('Settings.json'))
        self.maximumRank = self.settings["MaximumRank"]
        self.maximumUpgradeLevel = self.settings["MaximumUpgradeLevel"]
        self.requiredTrophiesForRank = ProgressStart = [0,10,20,30,40,60,80,100,120,140,160,180,220,260,300,340,380,420,460,500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200]
        if self.maximumRank <= 34:
            self.brawlersTrophies = self.requiredTrophiesForRank[self.maximumRank-1]
        else:
            self.brawlersTrophies = self.requiredTrophiesForRank[33] + (50* (self.maximumRank-34))
        self.writeVInt(2017189)  # Shop Timestamp
        self.writeVInt(100) # box cost (gold)
        self.writeVInt(10) # box cost (gems)
        self.writeVInt(80) # box cost (gems)
        self.writeVInt(10) # box cost (gems)
        self.writeVInt(20) # Coin Boost cost
        self.writeVInt(50) # Coin Boost %
        self.writeVInt(50) # Coin Doubler cost
        self.writeVInt(1000) # Coin Doubled
        self.writeVInt(7*24) # Coin Boost Hours
        self.writeVInt(self.brawlersTrophies) # Minimum Brawler Trophies For Season Reset
        self.writeVInt(50) # Brawler Trophy Loss Percentage in Season Reset
        self.writeVInt(9999) # Coin Limit Remaining
        self.writeArrayVInt([1,2,5,10,20,60]) # Duplicated Brawler Chips
        self.writeArrayVInt([3,10,20,60,200,500]) # Brawler Chip Cost
        self.writeArrayVInt([0,30,80,170,0,0]) # Boxes With Guaranteed Brawlers Cost
        # Events array starts

        # Brawlers required for events starts

        self.writeVInt(self.player.eventCount) # count

        requiredBrawlers = [0, 3, 5, 7]

        for event in range(self.player.eventCount):
            self.writeVInt(event + 1) # event index
            self.writeVInt(requiredBrawlers[event]) # Brawlers needed for that

        # Brawlers required for events ends

        # disponible events starts
        eventData = db.loadEvents(1)["info"]["events"]
        self.writeVInt(len(eventData)) # disponibles event slot
        index = 0
        for event in eventData:
            events = eventData[event]
            self.writeVInt(index + 1) # slot index
            self.writeVInt(index + 1) # slot number
            self.writeVInt(events["TimeStamp"] - int(time())) # comming soon timer
            self.writeVInt(events["TimeStamp"] - int(time())) # Time Left
            self.writeVInt(events["Tokens"]) # coins to claim
            self.writeVInt(8) # bonuska coins
            self.writeVInt(999) # coins to win
            self.writeBoolean(False) # double coins
            self.writeBoolean(index == 3) # double exp
            self.writeScID(15, events["ID"]) # map
            self.writeVInt(0) #  coins already collected
            self.writeVInt(2) #  coins collected statut
            self.writeString("Server by PrimoDEVHacc") # text for event (TID) please keep it for credits
            self.writeBoolean(False)
            index += 1

        # disponible events ends

        # comming soon events starts
        eventData = db.loadEvents(2)["info"]["events"]
        self.writeVInt(len(eventData)) # disponibles event slot
        index = 0
        for event in eventData:
            events = eventData[event]
            self.writeVInt(index + 1) # slot index
            self.writeVInt(index + 1) # slot number
            self.writeVInt(events["TimeStamp"] - int(time())) # comming soon timer
            self.writeVInt(events["TimeStamp"] - int(time())) # Time Left
            self.writeVInt(events["Tokens"]) # coins to claim
            self.writeVInt(8) # bonuska coins
            self.writeVInt(999) # coins to win
            self.writeBoolean(False) # double coins
            self.writeBoolean(index == 3) # double exp
            self.writeScID(15, events["ID"]) # map
            self.writeVInt(0) #  coins already collected
            self.writeVInt(2) #  coins collected statut
            self.writeString("Server by PrimoDEVHacc") # text for event (TID) please keep it for credits
            self.writeBoolean(False)
            index += 1
        # comming soon event ends
            
        # Events array ends

        self.writeVInt(self.maximumUpgradeLevel) # upgrades Array
        for x in range(self.maximumUpgradeLevel):
            self.writeVInt(x + 1) # price

        Milestones.MilestonesArray(self)