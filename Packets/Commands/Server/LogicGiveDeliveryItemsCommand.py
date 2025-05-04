
import random
from Files.CsvLogic.Cards import Cards
from Utils.Writer import Writer
from Database.DatabaseManager import DataBase
from datetime import datetime


class LogicGiveDeliveryItemsCommand(Writer):
    def __init__(self, device, player):
        super().__init__(device)
        self.player = player
        self.device = device
    def getBoxID(self, boxID):
       db = DataBase(self.player)
       if boxID == 1:
          if self.player.gold < 100:
                return "no cheating lol"
          self.player.gold -= 100
          db.replaceValue("gold", self.player.gold)
          return 10
       elif boxID == 2:
          if self.player.gems < 10:
                return "no cheating lol"
          self.player.gems -= 10
          db.replaceValue("gems", self.player.gems)
          return 10
       elif boxID == 3:
          if self.player.gems < 80:
                return "no cheating lol"
          self.player.gems -= 80
          db.replaceValue("gems", self.player.gems)
          return 11
       else:
          return boxID
    def rarityByID(self, rarity):
       if rarity == 0:
          return "common"
       elif rarity == 1:
          return "rare"
       elif rarity == 2:
          return "super_rare"
       elif rarity == 3:
          return "epic"
       elif rarity == 4:
          return "mega_epic"
       else:
          return "legendary"
       
    def generateRewardsForBrawlerBox(self, boxID):
       db = DataBase(self.player)
       self.rewards = {}
       self.rewards["boxID"] = boxID
       if boxID == 1:
          if self.player.gems < 30:
                return "no cheating lol"
          self.player.gems -= 30
          db.replaceValue("gems", self.player.gems)
       elif boxID == 2:
          if self.player.gems < 80:
                return "no cheating lol"
          self.player.gems -= 80
          db.replaceValue("gems", self.player.gems)
       elif boxID == 3:
          if self.player.gems < 170:
                return "no cheating lol"
          self.player.gems -= 170
          db.replaceValue("gems", self.player.gems)
       self.rewards["rewards"] = {}
       for reward in range(1):
          self.rewards["rewards"][reward] = {}
          self.rewards["rewards"][reward]["rarity"] = boxID
          selectedCharacters = Cards().getBrawlersWithRarity(self.rarityByID(boxID))
          selectedCharacters = [character for character in selectedCharacters if str(character) not in self.player.unlocked_brawlers]
          selectedCharacter = random.choice(selectedCharacters)
          self.rewards["rewards"][reward]["amount"] = 1
          self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
          self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
            'Cards': {selectedCharacter: 1},
            'Skins': [0],

            'selectedSkin': 0,
            'Trophies': 0,
            'HighestTrophies': 0,
            'PowerLevel': 0,
            'PowerPoints': 0,
            'State': 0,
            'StarPower': 0
         }
          db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
          self.rewards["rewards"][reward]["rewardID"] = 1
       return self.rewards
      
    def generateRewards(self, boxID):
       db = DataBase(self.player)
       self.rewards = {}
       self.rewards["boxID"] = self.getBoxID(boxID)
       if self.rewards["boxID"] == 11:
          rewardsAmount = 10
       else:
          rewardsAmount = 1
       self.rewards["rewards"] = {}
       for reward in range(rewardsAmount):
          self.rewards["rewards"][reward] = {}
          self.rewards["rewards"][reward]["rarity"] = random.choices([0, 1, 2, 3, 4, 5], weights=[25, 20, 15, 12, 8, 5], k=1)[0]
          if self.rewards["rewards"][reward]["rarity"] == 0:
             rewardList = ["Brawler", "Elexir"]
             selectedReward = random.choices(rewardList, weights= [10, 90], k=1)[0]
             if len(self.player.unlocked_brawlers) == 1:
                selectedReward = "Brawler"
             if selectedReward == "Elexir":
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 3
                self.player.elexir += 1
                db.replaceValue("elexir", self.player.elexir)
             else:
                selectedCharacter = random.choice(Cards().getBrawlersWithRarity("common"))
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                else:
                   self.player.chips += 1
                   db.replaceValue("chips", self.player.chips)
                   self.rewards["rewards"][reward]["rewardID"] = 2
                   
          elif self.rewards["rewards"][reward]["rarity"] == 1:
             rewardList = ["Brawler", "Elexir"]
             selectedReward = random.choices(rewardList, weights= [10, 90], k=1)[0]
             if selectedReward == "Elexir":
                self.rewards["rewards"][reward]["amount"] = 2
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 3
                self.player.elexir += 2
                db.replaceValue("elexir", self.player.elexir)
             else:
                selectedCharacter = random.choice(Cards().getBrawlersWithRarity("rare"))
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                else:
                   self.player.chips += 2
                   self.rewards["rewards"][reward]["amount"] = 2
                   db.replaceValue("chips", self.player.chips)
                   self.rewards["rewards"][reward]["rewardID"] = 2
                   
          elif self.rewards["rewards"][reward]["rarity"] == 2:
             rewardList = ["Brawler", "Elexir", "Doubler", "Booster"]
             selectedReward = random.choices(rewardList, weights= [10, 30, 30, 30], k=1)[0]
             if selectedReward == "Elexir":
                self.rewards["rewards"][reward]["amount"] = 3
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 3
                self.player.elexir += 3
                db.replaceValue("elexir", self.player.elexir)
             elif selectedReward == "Doubler":
                self.rewards["rewards"][reward]["amount"] = 200
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 4
                self.player.coinsdoubler += 200
                db.replaceValue("coinsdoubler", self.player.coinsdoubler)
             elif selectedReward == "Booster":
                self.rewards["rewards"][reward]["amount"] = 259200
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 5
                current_booster = self.player.coinsbooster
                if (int(datetime.timestamp(datetime.now())) - current_booster) <= 0:
                    self.player.coinsbooster = int(datetime.timestamp(datetime.now())) + 259200
                    db.replaceValue('coinsbooster', self.player.coinsbooster)
                else:
                    self.player.coinsbooster += 259200
                    db.replaceValue('coinsbooster', self.player.coinsbooster)
             else:
                selectedCharacter = random.choice(Cards().getBrawlersWithRarity("super_rare"))
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                else:
                   self.player.chips += 4
                   self.rewards["rewards"][reward]["amount"] = 4
                   db.replaceValue("chips", self.player.chips)
                   self.rewards["rewards"][reward]["rewardID"] = 2
          elif self.rewards["rewards"][reward]["rarity"] == 3:
             rewardList = ["Brawler", "Elexir"]
             selectedReward = random.choices(rewardList, weights= [10, 90], k=1)[0]
             if selectedReward == "Elexir":
                self.rewards["rewards"][reward]["amount"] = 5
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 3
                self.player.elexir += 5
                db.replaceValue("elexir", self.player.elexir)
             else:
                selectedCharacter = random.choice(Cards().getBrawlersWithRarity("epic"))
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                else:
                   self.player.chips += 10
                   self.rewards["rewards"][reward]["amount"] = 10
                   db.replaceValue("chips", self.player.chips)
                   self.rewards["rewards"][reward]["rewardID"] = 2
          elif self.rewards["rewards"][reward]["rarity"] == 4:
             rewardList = ["Brawler", "Elexir"]
             selectedReward = random.choices(rewardList, weights= [10, 90], k=1)[0]
             if selectedReward == "Elexir":
                self.rewards["rewards"][reward]["amount"] = 7
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 3
                self.player.elexir += 7
                db.replaceValue("elexir", self.player.elexir)
             else:
                selectedCharacter = random.choice(Cards().getBrawlersWithRarity("mega_epic"))
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                else:
                   self.player.chips += 25
                   self.rewards["rewards"][reward]["amount"] = 25
                   db.replaceValue("chips", self.player.chips)
                   self.rewards["rewards"][reward]["rewardID"] = 2
          elif self.rewards["rewards"][reward]["rarity"] == 5:
             rewardList = ["Brawler", "Elexir"]
             selectedReward = random.choices(rewardList, weights= [10, 90], k=1)[0]
             if selectedReward == "Elexir":
                self.rewards["rewards"][reward]["amount"] = 10
                self.rewards["rewards"][reward]["dataref"] = [23, 0]
                self.rewards["rewards"][reward]["rewardID"] = 3
                self.player.elexir += 10
                db.replaceValue("elexir", self.player.elexir)
             else:
                selectedCharacter = random.choice(Cards().getBrawlersWithRarity("legendary"))
                self.rewards["rewards"][reward]["amount"] = 1
                self.rewards["rewards"][reward]["dataref"] = [23, selectedCharacter]
                if str(Cards().getbrawlerID(selectedCharacter)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(selectedCharacter)] = {
                     'Cards': {selectedCharacter: 1},
                     'Skins': [0],

                     'selectedSkin': 0,
                     'Trophies': 0,
                     'HighestTrophies': 0,
                     'PowerLevel': 0,
                     'PowerPoints': 0,
                     'State': 0,
                     'StarPower': 0
                  }
                   db.replaceValue('unlocked_brawlers', self.player.unlocked_brawlers)
                   self.rewards["rewards"][reward]["rewardID"] = 1
                else:
                   self.player.chips += 60
                   self.rewards["rewards"][reward]["amount"] = 60
                   db.replaceValue("chips", self.player.chips)
                   self.rewards["rewards"][reward]["rewardID"] = 2
          db.loadAccount()
       return self.rewards
    def encode(self, rewards):
          self.rewards = rewards
          db = DataBase(self.player)
          self.writeVInt(self.rewards["boxID"]) # box id
          self.writeVInt(len(self.rewards["rewards"])) # reward amount
          for reward in self.rewards["rewards"]:
            self.writeVInt(self.rewards["rewards"][reward]["rarity"]) # rarity
            self.writeVInt(self.rewards["rewards"][reward]["amount"]) # amount
            self.writeScID(self.rewards["rewards"][reward]["dataref"][0], self.rewards["rewards"][reward]["dataref"][1]) # item type

            self.writeVInt(self.rewards["rewards"][reward]["rewardID"]) # item given
            

"""
    def decode(self):
        logicGiveDeliveryItemsPayload = {}
        logicGiveDeliveryItemsPayload["rarityID"] = self.readVInt()
        logicGiveDeliveryItemsPayload["itemTypeID"] = self.readDataReference()
        logicGiveDeliveryItemsPayload["rewardAmount"] = self.readVInt()
        logicGiveDeliveryItemsPayload["itemClassID"] = self.readDataReference()
    def process(self):
        pass
"""
