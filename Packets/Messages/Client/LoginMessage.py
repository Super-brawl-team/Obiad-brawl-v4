from Utils.Reader import ByteStream
from Packets.Messages.Server.LoginOkMessage import LoginOkMessage
from Packets.Messages.Server.LoginFailedMessage import LoginFailedMessage
from Packets.Messages.Server.OwnHomeDataMessage import OwnHomeDataMessage
from Packets.Messages.Server.ClanData import ClanData
from Packets.Messages.Server.ClanStream import ClanStream
from Logic.Player import Player
from Database.DatabaseManager import DataBase
from Utils.Helpers import Helpers
import time
class LoginMessage(ByteStream):

    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player

    def decode(self):
        self.loginPayload = {}
        self.loginPayload["highID"] = self.readInt()
        self.loginPayload["lowID"] = self.readInt()
        self.loginPayload["token"] = self.readString()
        self.loginPayload["majorVersion"] = self.readInt()
        self.loginPayload["minorVersion"] = self.readInt()
        self.loginPayload["build"] = self.readInt()
        self.loginPayload["fingerprintSHA"] = self.readString()
        self.loginPayload["unknownString1"] = self.readString()
        self.loginPayload["deviceID"] = self.readString()
        self.loginPayload["unknownString2"] = self.readString()
        self.loginPayload["device"] = self.readString()
        self.loginPayload["systemLanguage"] = self.readVInt()
        self.loginPayload["region"] = self.loginPayload["systemLanguage"] = self.readString().split('-')[1]
        self.player.usedVersion = self.loginPayload["majorVersion"]

    def process(self):
        db = DataBase(self.player)
        print(self.loginPayload["token"])
        if self.player.usedVersion == 4:
            if not db.is_token_in_table(self.loginPayload["token"]):
                if self.loginPayload["token"] is None:
                    self.loginPayload["token"] = self.player.token = Helpers.randomStringDigits(self)
                else:
                    self.player.token = self.loginPayload["token"]
                db.getPlayerId()
                db.createAccount()
                


            # Process login information
            self.player.high_d = self.loginPayload["highID"]
            self.player.low_id = self.loginPayload["lowID"]
            self.player.token = str(self.loginPayload["token"])
            self.player.region = self.loginPayload["region"]
            db.replaceValue("region", self.player.region)

            # Send success messages
            LoginOkMessage(self.device, self.player, self.loginPayload).Send()
            ClanStream(self.device, self.player).Send()  # 14109
            OwnHomeDataMessage(self.device, self.player).Send()
            ClanData(self.device, self.player).Send()  # 14109
        else:
            LoginFailedMessage(self.device, self.player, self.loginPayload, " ", 16)