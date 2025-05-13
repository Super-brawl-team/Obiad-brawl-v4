from Utils.Writer import Writer
from Database.DatabaseManager import DataBase

class LogicAddNotificationCommand(Writer):

    def __init__(self, device, player):
        super().__init__(device)
        self.id = 24111
        self.player = player
        self.device = device


    def encode(self, key):
        self.writeBoolean(True)
        if True:
            db = DataBase(self.player)
            notif = self.player.homeNotifications[str(key)]
            self.writeVInt(notif["ID"]) # notif id 97 (expired coins booster), 98 (gatcha drop or someshit) or 99 (season end)
            if notif["ID"] == 97:
                self.writeVInt(notif["type"])
            elif notif["ID"] == 98:
                self.writeVInt(1) # unk
                self.writeVInt(2) # unk
            elif notif["ID"] == 99:
                # region 1
                self.writeVInt(1) # total best brawler trophies i guess
                self.writeVInt(notif["bestBrawlerPoints"]) # total season points for the best hero
                self.writeVInt(notif["bestBrawlerCoins"]) # coins gained for the best hero
                self.writeVInt(notif["bestBrawlerBonus"]) # bonus coins gained for the best hero
                # end
                # region 2
                self.writeVInt(notif["totalTrophies"]) # total trophies
                self.writeVInt(notif["totalTrophiesPoints"]) # total trophies total points
                self.writeVInt(notif["totalTrophiesCoins"]) # total trophies gained coins
                self.writeVInt(notif["totalTrophiesBonus"]) # total trophies gained bonus
                # end
                self.writeVInt(1) # idk
                self.writeVInt(1) # idk
                self.writeDataReference(16, notif["bestBrawler"]) # best braler
                self.writeVInt(1) # idk
                self.writeVInt(1) # idk
            del self.player.homeNotifications[key]
            db.replaceValue("homeNotifications", self.player.homeNotifications)