
import random
from Files.CsvLogic.Cards import Cards
from Utils.Reader import ByteStream
from Database.DatabaseManager import DataBase
class LogicGiveDeliveryItemsCommand(ByteStream):
    def __init__(self, device, player, data):
        super().__init__(data)
        self.player = player
        self.device = device
        self.isDuplicated = False
    def encode(self):
          self.isDuplicated = False
          db = DataBase(self.player)
          randomValue1 = random.randint(0, 1)
          self.writeVInt(10) # box id
          self.writeVInt(1) # reward amount

          if randomValue1 == 1:

          
                Elixir = random.randint(0, 3)
                if Elixir == 0:
                   Amount = 1
                   Rarity = 0
                elif Elixir == 1:
                   Amount = 2
                   Rarity = 1
                elif Elixir == 2:
                   Amount = 5
                   Rarity = 2
                elif Elixir == 3:
                   Amount = 10
                   Rarity = 3
            
           
                self.writeVInt(Rarity) # rarity
                self.writeVInt(Amount) # amount
                self.writeScID(23, 0) # item type

                self.writeVInt(3) # item given
                self.player.elexir += Amount
                db.replaceValue("elexir", self.player.elexir)
          else:
                chipsList = [1, 2, 10, 60]
                BrawlersList = Cards().getBrawlers()
                Brawler = (random.choice(BrawlersList))
                Rarity = Cards().getBrawlerRarity(Brawler)
                if Rarity == 'common':
                   RarityID = 0
                elif Rarity == 'rare':
                   RarityID = 1
                elif Rarity == 'epic':
                   RarityID = 2
                else:
                   RarityID = 3
                if str(Cards().getbrawlerID(Brawler)) not in self.player.unlocked_brawlers:
                   self.player.unlocked_brawlers[Cards().getbrawlerID(Brawler)] = {
                     'Cards': {Brawler: 1},
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
                else:
                   self.player.chips += chipsList[RarityID]
                   db.replaceValue("chips", self.player.chips)
                   self.isDuplicated = True
                self.writeVInt(RarityID) # rarity ID
                self.writeVInt(1)
                self.writeScID(23, Brawler)

                self.writeVInt(2 if self.isDuplicated else 1)


    def decode(self):
        logicGiveDeliveryItemsPayload = {}
        logicGiveDeliveryItemsPayload["rarityID"] = self.readVInt()
        logicGiveDeliveryItemsPayload["itemTypeID"] = self.readDataReference()
        logicGiveDeliveryItemsPayload["rewardAmount"] = self.readVInt()
        logicGiveDeliveryItemsPayload["itemClassID"] = self.readDataReference()
    def process(self):
        pass
