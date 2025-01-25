# -*- coding: utf-8 -*-

from Utils.Reader import ByteStream
from Utils.Writer import Writer
from Logic.Player import Player
from Packets.LogicCommandManager import commands


class EndClientTurnMessage(ByteStream):

    def __init__(self, data, device, player):
        super().__init__(data)
        self.device = device
        self.data = data
        self.player = player

    def decode(self):
        self.endClientTurn = {}
        self.endClientTurn["isCommand"] = self.readBoolean()
        self.endClientTurn["unk"] = self.readVInt()
        self.endClientTurn["unk2"] = self.readVInt()
        self.endClientTurn["commandAmount"] = self.readVInt()
        self.endClientTurn["commandID"] = self.readVInt()

    def process(self):
        if self.endClientTurn["commandID"] in commands:
                print("[*]", self.endClientTurn["commandID"], "received")
                command = commands[self.endClientTurn["commandID"]](self.device, self.player, self.data)
                command.decode()
                command.process()
        elif self.endClientTurn["commandID"] > 0:
                print("[*] ", self.endClientTurn["commandID"], "not handled")  
        else:
                print("[*] A negative length command got recieved")    