# -*- coding: utf-8 -*-

from Packets.Messages.Server.KeepAliveOkMessage import KeepAliveOkMessage
from Utils.Reader import ByteStream
from Packets.Messages.Server.MyAlliance import MyAlliance
from datetime import datetime
from Packets.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
from Database.DatabaseManager import DataBase

class KeepAliveMessage(ByteStream):

    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player

    def decode(self):
        pass

    def process(self):
        KeepAliveOkMessage(self.device, self.player).Send()
        try: 
            db = DataBase(self.player)
            MyAlliance(self.device, self.player).Send()
            if self.player.coinsbooster - int(datetime.timestamp(datetime.now())) <= 0 and self.player.player_status == 2:
                for x in self.player.homeNotifications:
                    notif = self.player.homeNotifications[x]
                    if notif["ID"] ==97 and notif["type"] ==1:
                        return
                key = len(self.player.homeNotifications)
                self.player.homeNotifications[key] = {"ID": 97, "type": 1, "seen": False}
                db.replaceValue("homeNotifications", self.player.homeNotifications)
                AvailableServerCommandMessage(self.device, self.player, 204, key)
        except:
            pass
