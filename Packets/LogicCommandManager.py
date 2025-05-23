from Packets.Commands.Client.LogicGatchaCommand import LogicGatchaCommand
from Packets.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand
from Packets.Commands.Client.LogicBuyCard import LogicBuyCardCommand
from Packets.Commands.Client.LogicSelectBattleHints import LogicSelectBattleHintsCommand
from Packets.Commands.Client.LogicSelectControlMode import LogicSelectControlModeCommand
from Packets.Commands.Client.LogicSetPlayerThumbnailCommand import LogicSetPlayerThumbnailCommand
from Packets.Commands.Client.LogicBuyBrawlerCommand import LogicBuyBrawlerCommand
from Packets.Commands.Client.LogicBuyCoinsBoosterCommand import LogicBuyCoinsBoosterCommand
from Packets.Commands.Client.LogicBuyCoinsDoublerCommand import LogicBuyCoinsDoublerCommand
from Packets.Commands.Client.LogicUnlockSkinCommand import LogicUnlockSkinCommand
from Packets.Commands.Client.LogicHandleNotificationCommand import LogicHandleNotificationCommand
commands = {
    #203: LogicGiveDeliveryItemsCommand,
    500: LogicGatchaCommand,
    502: LogicBuyCardCommand,
    506: LogicSetPlayerThumbnailCommand,
    508: LogicUnlockSkinCommand,
    509: LogicSelectControlModeCommand,
    510: LogicBuyCoinsDoublerCommand,
    511: LogicBuyCoinsBoosterCommand,
    513: LogicSelectBattleHintsCommand,
    514: LogicBuyBrawlerCommand,
    515: LogicHandleNotificationCommand
}