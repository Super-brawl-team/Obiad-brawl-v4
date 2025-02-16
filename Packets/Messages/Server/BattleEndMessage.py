# -*- coding: utf-8 -*-
from Utils.Writer import Writer

from Logic.Milestones import Milestones
from Database.DatabaseManager import DataBase
from Files.CsvLogic.Cards import Cards
from Files.CsvLogic.Characters import Characters
import json
from datetime import datetime
class BattleEndSD(Writer):

	def __init__(self, device, player, plrs):
		self.id = 23456
		self.device = device
		self.player = player
		self.plrs = plrs
		super().__init__(self.device)

	def encode(self):
     	
		def getBattleEndTrophies(rang, trophies):
			
			trophy_ranges = [
				(0, 29, [8, 7, 6, 5, 5, 4, 3, 2, 1, 0]),
				(30, 59, [8, 7, 6, 4, 3, 2, 0, -1, -2, -4]),
				(60, 99, [8, 7, 5, 4, 3, 1, 0, -2, -3, -4]),
				(100, 139, [7, 6, 5, 3, 2, 1, -1, -2, -3, -4]),
				(140, 219, [7, 6, 4, 3, 2, 0, -1, -3, -4, -5]),
				(220, 299, [7, 6, 4, 3, 1, 0, -2, -3, -5, -6]),
				(300, 419, [7, 6, 4, 2, 1, -1, -2, -4, -6, -7]),
				(420, 499, [5, 4, 3, 1, 0, -2, -3, -4, -6, -7]),
				(500, 599, [5, 3, 2, 1, -1, -2, -3, -4, -6, -7]),
				(600, 699, [4, 3, 1, 0, -1, -1, -3, -5, -6, -7]),
				(700, 799, [4, 2, 1, -1, -2, -3, -4, -5, -6, -8]),
				(800, 899, [3, 2, 0, -1, -2, -3, -4, -5, -7, -8]),
				(900, float("inf"), [3, 1, -1, -2, -3, -4, -5, -6, -7, -8]),
				
			]
			for low, high, rank_trophies in trophy_ranges:
				if low <= trophies <= high:
					return rank_trophies[rang-1]
			return 0
		
		def getBattleEndCoins(rang):
			if rang == 10:
				return 1
			elif rang == 9:
				return 1
			elif rang == 8:
				return 2
			elif rang == 7:
				return 4
			elif rang == 6:
				return 6
			elif rang == 5:
				return 8
			elif rang == 4:
				return 12
			elif rang == 3:
				return 16
			elif rang == 2:
				return 22
			elif rang == 1:
				return 28
			elif rang == 0:
				return 34
		
		def getBattleEndExp(rang):
			if rang == 10:
				return 0
			elif rang == 9:
				return 0
			elif rang == 8:
				return 0
			elif rang == 7:
				return 1
			elif rang == 6:
				return 2
			elif rang == 5:
				return 4
			elif rang == 4:
				return 5
			elif rang == 3:
				return 6
			elif rang == 2:
				return 9
			elif rang == 1:
				return 12
			elif rang == 0:
				return 15

		db = DataBase(self.player)
		if not self.plrs["isInRealGame"]:
			trophies = 0
			coins = 0
			exp = 0
			star_player_exp = 0
			doubled_coins = 0
			boosted_coins = 0
		else:
			trophies = getBattleEndTrophies(self.plrs["BattleRank"], self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"])
			coins = getBattleEndCoins(self.plrs["BattleRank"])
			exp = getBattleEndExp(self.plrs["BattleRank"])
			star_player_exp = 10
			doubled_coins = coins
			if coins > self.player.coinsdoubler:
				doubled_coins = self.player.coinsdoubler
			self.player.coinsdoubler -= doubled_coins
			db.replaceValue("coinsdoubler", self.player.coinsdoubler)
			boosted_coins = 0
			if self.player.coinsbooster  - int(datetime.timestamp(datetime.now())) > 0:
				boosted_coins = coins
		self.writeVInt(5) # Battle End Game Mode (5 = Showdown. Else is 3vs3)
		self.writeVInt(0) # Related To Coins Gained. If the Value is 1+, "All Coins collected"
		self.writeVInt(coins) # Coins Gained
		self.writeVInt(6969) # "All Coins collected" if 0, its basically coins left
		self.writeVInt(0) # First Win Coins Gained
		self.writeBool(False) # "All event experience collected" if True
		self.writeVInt(self.plrs["BattleRank"]) # Result (Victory/Defeat/Draw/Rank Score)
		
		self.writeVInt(trophies) # Trophies Result
		self.writeScID(28, self.player.profile_icon)  # Player Profile Icon
		self.writeBoolean(False) # is tutorial game
		self.writeBoolean(self.plrs["isInRealGame"]) # is in real game
		self.writeVInt(50) # Coin Booster %
		self.writeVInt(boosted_coins) # Coin Booster Coins Gained
		self.writeVInt(doubled_coins) # Coin Doubler Coins Gained
		
		# Players Array

		self.writeVInt(self.plrs["PlayersAmount"]) # Battle End Screen Players
		for Players in self.plrs["Brawlers"]:
			self.writeString(Players["Name"]) # Player Name
			self.writeBoolean(Players["IsPlayer"]) # is player
			self.writeBoolean(Players["Team"] is not self.plrs["Brawlers"][0]["Team"]) # is ennemy?
			self.writeBoolean(Players["IsPlayer"]) # is star player
			self.writeScID(Players["CharacterID"][0], Players["CharacterID"][1]) # Player Brawler
			self.writeScID(Players["SkinID"][0], Players["SkinID"][1]) # Player Brawler Skin!
			self.writeVInt(0) # Brawler Trophies
			self.writeVInt(Players["powerLevel"]-1) # Brawler power level
		# Experience Array
		self.writeVInt(2) # Count
		self.writeVInt(0) # Normal Experience ID
		self.writeVInt(exp) # Normal Experience Gained
		self.writeVInt(8) # Star Player Experience ID
		self.writeVInt(star_player_exp) # Star Player Experience Gained

		# Rank Up and Level Up Bonus Array
		self.writeVInt(0) # Count

		# Trophies and Experience Bars Array
		self.writeVInt(2) # Count
		self.writeVInt(1) # Trophies Bar Milestone ID
		self.writeVInt(self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]) # Brawler Trophies
		self.writeVInt(self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]) # Brawler Trophies for Rank
		self.writeVInt(5) # Experience Bar Milestone ID
		self.writeVInt(self.player.player_experience) # Player Experience
		self.writeVInt(self.player.player_experience) # Player Experience for Level
		
		# Milestones Array
		self.writeBool(True) # Bool

		Milestones.MilestonesArray(self)
		self.player.trophies += trophies
		db.replaceValue("trophies", self.player.trophies)
		if self.player.club_id != 0:
			db.incrementClubTrophies(trophies)
		self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] += trophies
		if self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] > self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]:
			self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"] = self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]
		db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
		self.player.player_experience += exp + star_player_exp
		db.replaceValue("player_experience", self.player.player_experience)
		self.player.gold += coins+boosted_coins+doubled_coins
		db.replaceValue("gold", self.player.gold)
		self.player.coins_reward = coins+doubled_coins+boosted_coins 
		db.replaceValue("coins_reward", self.player.coins_reward)
		
		
class BattleEndTrio(Writer):

	def __init__(self, device, player, plrs):
		self.id = 23456
		self.device = device
		self.plrs = plrs
		self.player = player

		super().__init__(self.device)

	def encode(self):
		def getBattleEndTrophies(rang, trophies):
			
			trophy_ranges = [
				(0, 29, [6, 0, 0]),
				(30, 59, [6, -1, 0]),
				(60, 99, [6, -2, 0]),
				(100, 139, [5, -2, 0]),
				(140, 219, [5, -3, 0]),
				(220, 299, [5, -4, 0]),
				(300, 499, [5, -5, 0]),
				(500, 599, [4, -6, 0]),
				(600, 699, [3, -6, 0]),
				(700, 799, [3, -7, 0]),
				(800, 899, [2, -7, 0]),
				(900, float("inf"), [2, -8, 0]),
				
			]
			for low, high, rank_trophies in trophy_ranges:
				if low <= trophies <= high:
					return rank_trophies[rang]
			return 0
		
		
		def getBattleEndCoins(rang):
			if rang == 0: # win
				return 20
			elif rang == 1:
				return 15
			elif rang == 2:
				return 10

		def getBattleEndExp(rang):
			if rang == 0: # win
				return 10
			elif rang == 1:
				return 5
			elif rang == 2:
				return 0

		db = DataBase(self.player)
		if not self.plrs["isInRealGame"]:
			trophies = 0
			coins = 0
			exp = 0
			star_player_exp = 0
			doubled_coins = 0
			boosted_coins = 0
		else:
			trophies = getBattleEndTrophies(self.plrs["BattleRank"], self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"])
			coins = getBattleEndCoins(self.plrs["BattleRank"])
			exp = getBattleEndExp(self.plrs["BattleRank"])
			star_player_exp = 10
			doubled_coins = coins
			if coins > self.player.coinsdoubler:
				doubled_coins = self.player.coinsdoubler
			self.player.coinsdoubler -= doubled_coins
			db.replaceValue("coinsdoubler", self.player.coinsdoubler)
			boosted_coins = 0
			if self.player.coinsbooster  - int(datetime.timestamp(datetime.now())) > 0:
				boosted_coins = coins

		# Star Player State End

		self.writeVInt(1) # Battle End Game Mode (5 = Showdown. Else is 3vs3)
		self.writeVInt(0) # Related To Coins Gained. If the Value is 1+, "All Coins collected"

		self.writeVInt(coins) # Coins Gained
		self.writeVInt(6969) # "All Coins collected" if 0, its basically coins left
		self.writeVInt(0) # First Win Coins Gained
		self.writeBool(False) # "All event experience collected" if True
		self.writeVInt(self.plrs["BattleEndType"]) # Result (Victory/Defeat/Draw/Rank Score)
		self.writeVInt(trophies) # Trophies Result
		self.writeScID(28, self.player.profile_icon)  # Player Profile Icon
		self.writeBoolean(False) # is tutorial game
		self.writeBoolean(self.plrs["isInRealGame"]) # is in real game
		self.writeVInt(50) # Coin Booster %
		self.writeVInt(boosted_coins) # Coin Booster Coins Gained
		self.writeVInt(doubled_coins) # Coin Doubler Coins Gained

		# Players Array

		self.writeVInt(self.plrs["PlayersAmount"]) # Battle End Screen Players
		for Players in self.plrs["Brawlers"]:
			self.writeString(Players["Name"]) # Player Name
			self.writeBoolean(Players["IsPlayer"]) # is player
			self.writeBoolean(Players["Team"] is not self.plrs["Brawlers"][0]["Team"]) # is ennemy?
			self.writeBoolean(Players["IsPlayer"]) # is star player
			self.writeScID(Players["CharacterID"][0], Players["CharacterID"][1]) # Player Brawler
			self.writeScID(Players["SkinID"][0], Players["SkinID"][1]) # Player Brawler Skin!
			self.writeVInt(0) # Brawler Trophies
			self.writeVInt(Players["powerLevel"]-1) # Brawler power level
		# Experience Array
		self.writeVInt(2) # Count
		self.writeVInt(0) # Normal Experience ID
		self.writeVInt(exp) # Normal Experience Gained
		self.writeVInt(8) # Star Player Experience ID
		self.writeVInt(star_player_exp) # Star Player Experience Gained

		# Rank Up and Level Up Bonus Array
		self.writeVInt(0) # Count

		# Trophies and Experience Bars Array
		self.writeVInt(2) # Count
		self.writeVInt(1) # Trophies Bar Milestone ID

		self.writeVInt(self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]) # Brawler Trophies
		self.writeVInt(self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]) # Brawler Trophies for Rank
		self.writeVInt(5) # Experience Bar Milestone ID
		self.writeVInt(self.player.player_experience) # Player Experience
		self.writeVInt(self.player.player_experience) # Player Experience for Level
		self.player.trophies += trophies
		db.replaceValue("trophies", self.player.trophies)
		if self.player.club_id != 0:
			db.incrementClubTrophies(trophies)
		self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] += trophies
		if self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"] > self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"]:
			self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["HighestTrophies"] = self.player.unlocked_brawlers[str(self.plrs["Brawlers"][0]["CharacterID"][1])]["Trophies"]
		db.replaceValue("unlocked_brawlers", self.player.unlocked_brawlers)
		self.player.player_experience += exp + star_player_exp
		db.replaceValue("player_experience", self.player.player_experience)
		self.player.gold += coins +boosted_coins+doubled_coins
		db.replaceValue("gold", self.player.gold)
		self.player.coins_reward = coins+boosted_coins+doubled_coins
		db.replaceValue("coins_reward", self.player.coins_reward)
		# Milestones Array
		self.writeBool(True) # Bool
		Milestones.MilestonesArray(self)