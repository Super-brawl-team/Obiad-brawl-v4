from Logic.Player import Player
from Packets.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
from Database.DatabaseManager import DataBase
from Utils.Reader import ByteStream
from Packets.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
class LogicHandleNotificationCommand(ByteStream):
    def __init__(self, device, player, data):
        super().__init__(data)
        self.player = player
        self.device = device

    def decode(self):
        self.readCommandHeader()
        self.id = self.readVInt()

    def process(self):
        db = DataBase(self.player)
        toClear = []
        if self.id == 1:
            for key in self.player.homeNotifications:
                notif = self.player.homeNotifications[key]
                if notif["ID"]==99:
                    self.player.homeNotifications[key]["seen"]= True
                    db.replaceValue("homeNotifications", self.player.homeNotifications)
                    toClear.append(key)
        elif self.id == 2:
            for key in self.player.homeNotifications:
                notif = self.player.homeNotifications[key]
                if notif["ID"]==97 and notif["type"]==2:
                    self.player.homeNotifications[key]["seen"]= True
                    db.replaceValue("homeNotifications", self.player.homeNotifications)
        elif self.id == 3:
            for key in self.player.homeNotifications:
                notif = self.player.homeNotifications[key]
                if notif["ID"]==97 and notif["type"]==1:
                    self.player.homeNotifications[key]["seen"]= True
                    db.replaceValue("homeNotifications", self.player.homeNotifications)
        elif self.id == 4:
            for key in self.player.homeNotifications:
                notif = self.player.homeNotifications[key]
                if notif["ID"]==98:
                    """Send LogicGiveDeliveryItems with your own rewards list here"""
                    self.player.homeNotifications[key]["seen"]= True
                    db.replaceValue("homeNotifications", self.player.homeNotifications)
                    toClear.append(key)
        for x in toClear:
            del self.player.homeNotifications[x]
            db.replaceValue("homeNotifications", self.player.homeNotifications)