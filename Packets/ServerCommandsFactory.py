from Packets.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
from Packets.Commands.Server.LogicChangeAvatarNameCommand import LogicChangeAvatarNameCommand
commands = {
    201: LogicChangeAvatarNameCommand,
    203: LogicGiveDeliveryItemsCommand
}