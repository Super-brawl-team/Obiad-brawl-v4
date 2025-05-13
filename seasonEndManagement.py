import json
import time
from Database.DatabaseManager import DataBase
from Packets.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
class SeasonEndManagement:
    @staticmethod
    def handleTrophies():
        db = DataBase(None)
        all_players = db.getAllPlayers()
        settings = json.load(open("Settings.json"))
        for player in all_players:
            unlocked = player["unlocked_brawlers"]
            if isinstance(unlocked, str):
                unlocked = json.loads(unlocked)

            updated_brawlers = {}
            best_brawler_id = None
            best_brawler_removal = 0
            total_removal = 0

            for brawler_id, brawler_data in unlocked.items():
                trophies = brawler_data["Trophies"]
                if trophies > 501:
                    removal = (trophies - 500) // 2
                    brawler_data["Trophies"] -= removal
                    total_removal += removal

                    if removal > best_brawler_removal:
                        best_brawler_removal = removal
                        best_brawler_id = int(brawler_id)
                    player["trophies"]-= removal
                elif trophies == 501:
                    removal = 1
                    brawler_data["Trophies"] -= removal
                    total_removal += removal

                    if removal > best_brawler_removal:
                        best_brawler_removal = removal
                        best_brawler_id = int(brawler_id)
                    player["trophies"]-= removal

                updated_brawlers[brawler_id] = brawler_data
            db.replaceOtherValue("trophies", player["trophies"], db.getTokenByLowId(player["low_id"]))
            db.replaceOtherValue("unlocked_brawlers", updated_brawlers, db.getTokenByLowId(player["low_id"]))
            if total_removal != 0:
                notification = {
                    "ID": 99,
                    "bestBrawlerPoints": best_brawler_removal,
                    "bestBrawlerCoins": best_brawler_removal,
                    "bestBrawlerBonus": settings["seasonEndBonus"],
                    "totalTrophiesPoints": total_removal,
                    "totalTrophiesCoins": total_removal,
                    "totalTrophiesBonus": settings["seasonEndBonus"], 
                    "bestBrawler": best_brawler_id or 0,
                    "seen": False
                }

                home_notifications = player.get("homeNotifications", {})
                if isinstance(home_notifications, str):
                    home_notifications = json.loads(home_notifications)
                index = str(len(home_notifications))
                home_notifications[index] = notification

                db.replaceOtherValue("homeNotifications", home_notifications, db.getTokenByLowId(player["low_id"]))
                player["gold"] += total_removal+ settings["seasonEndBonus"]*2
                db.replaceOtherValue("gold", player["gold"], db.getTokenByLowId(player["low_id"]))
                player["coins_reward"] += total_removal+ settings["seasonEndBonus"]*2
                db.replaceOtherValue("coins_reward", player["coins_reward"], db.getTokenByLowId(player["low_id"]))
                
        with open("Settings.json", "r") as f:
                settings = json.load(f)
        settings["nextSeasonEndTimestamp"] = int(time.time() + 1209600)
        with open("Settings.json", "w") as f:
            json.dump(settings, f, indent=4)
