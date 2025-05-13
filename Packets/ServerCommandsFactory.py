from Packets.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
from Packets.Commands.Server.LogicChangeAvatarNameCommand import LogicChangeAvatarNameCommand
from Packets.Commands.Server.LogicDiamondsAddedCommand import LogicDiamondsAddedCommand
from Packets.Commands.Server.LogicAddNotificationCommand import LogicAddNotificationCommand
from Packets.Commands.Server.LogicDayChangedCommand import LogicDayChangedCommand

commands = {
    201: LogicChangeAvatarNameCommand,
    202: LogicDiamondsAddedCommand,
    203: LogicGiveDeliveryItemsCommand,
    204: LogicDayChangedCommand,
    206: LogicAddNotificationCommand
}