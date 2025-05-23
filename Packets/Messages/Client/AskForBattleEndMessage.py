from Packets.Messages.Server.BattleEndMessage import *
from Files.CsvLogic.Locations import Locations
from Utils.Reader import ByteStream
from Files.CsvLogic.Cards import Cards

class AskForBattleEndMessage(ByteStream):

	def __init__(self, data, device, player):
		super().__init__(data)
		self.device = device
		self.data = data
		self.player = player

	def decode(self):
		self.plrs = {}
		self.plrs["BattleEndType"] = self.readVInt() # battle result
		self.plrs["BattleTime"] = self.readVInt() # time played ?

		self.plrs["BattleRank"] = self.readVInt() # rank so basically is won/lose/draw for 3v3 and the rank for sd
		self.plrs["CsvID0"] = self.readVInt() # secndary event index
		self.plrs["Location"] = self.readVInt() # actually its index of event
		self.plrs["PlayersAmount"] = self.readVInt() # Battle End Players
		self.plrs["Brawlers"] = []
		for x in range(self.plrs["PlayersAmount"]):
		# HeroDataEntry::encode
			self.plrs["Brawlers"].append({
				"CharacterID": self.readDataReference(),
				"SkinID": self.readDataReference(),
				"Team": self.readVInt(),
				"IsPlayer": self.readBoolean(), 
				"Name": self.readString(),
				"powerLevel": 0
			})

		for card, amount in self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Cards"].items():
			if not Cards().isUnlock(card):
				self.plrs["Brawlers"][0]["powerLevel"] += amount
		self.plrs["isInRealGame"] = True
	def process(self):
		db = DataBase(self.player)
		eventsData = db.loadEvents(1)["info"]["events"]
		if Locations().GetGamemode(eventsData[str(self.plrs["Location"]-1)]["ID"]) == "BossFight":
			BattleEndSD(self.device, self.player, self.plrs).Send()
		elif self.plrs["BattleRank"] != 0: # showdown
			BattleEndSD(self.device, self.player, self.plrs).Send()
		else:
			BattleEndTrio(self.device, self.player, self.plrs).Send()