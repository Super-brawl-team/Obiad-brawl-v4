# -*- coding: utf-8 -*-
from Entries.StreamEntryFactory import StreamEntryFactory
from Database.DatabaseManager import DataBase
from Utils.Writer import Writer

class ClanStream(Writer):
     def __init__(self, device, player):
          self.id = 24311
          self.device = device
          self.player = player
          super().__init__(self.device)

     def encode(self):
          db = DataBase(self.player)
          msgCount = 0
          clubMessages = None
          if self.player.club_id != 0:
               clubMessages = db.loadClubMessages(self.player.club_id)
          if clubMessages != None:
               msgCount = len(clubMessages["info"]["messages"])
          self.writeVint(msgCount)  # Message count
          #self.writeVInt(0)

          for index in range(msgCount):  # Loop through message indices
          #for index in range(0):
               messageKey = str(index)
               message = clubMessages["info"]["messages"][messageKey]
               self.writeVInt(message["EventType"])
               StreamEntryFactory.createStreamEntryByType(self, message)
          else:
               self.writeVint(0)  # No messages