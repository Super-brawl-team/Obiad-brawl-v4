from Packets.Messages.Server.TeamLeftMessage import TeamLeftMessage
from Utils.Reader import ByteStream
from Logic.Player import Player
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.TeamChatServerMessage import TeamStreamMessage
from Packets.Messages.Server.TeamMessage import TeamMessage

class TeamLeaveMessage(ByteStream):
    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player


    def decode(self):
        pass
        

    def process(self):
        if self.player.teamID == 0:
            return "kek"
        
        db = DataBase(self.player)
        db.addGameroomMsg(self.player.teamID, 4, self.player.low_id, self.player.name, "", 103, self.player.low_id, self.player.name)
        tick = db.getNextGameroomKey(self.player.teamID)
        db.loadGameroom()
        gameroomInfo = db.getGameroomInfo("info")
        for player_key, values in gameroomInfo["players"].items():
                TeamStreamMessage(self.device, self.player, tick).SendTo(player_key)
                TeamMessage(self.device, self.player).SendTo(player_key)
        db.removeGameroomPlayer(self.player.low_id, self.player.teamID, self.player.token)
        self.player.teamID = 0
        db.replaceValue("teamID", self.player.teamID)
        TeamLeftMessage(self.device, self.player, 0).Send()
        