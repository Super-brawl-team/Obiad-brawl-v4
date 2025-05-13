import csv

class Locations:
    def GetLocations(self):
        LocationsID = []

        with open('GameAssets/csv_logic/locations.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) 
            next(csv_reader)
            line_count = 0
            for row in csv_reader:
                if row[0] != "Tutorial":
                        LocationsID.append(line_count)
                line_count += 1

            return LocationsID
        
    def GetGamemode(self, ID):
        Gamemode = "CoinRush"

        with open('GameAssets/csv_logic/locations.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) 
            next(csv_reader)
            line_count = 0
            for row in csv_reader:
                if line_count == ID:
                        Gamemode = row[11]
                        break
                line_count += 1

            return Gamemode