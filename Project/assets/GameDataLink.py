import json

#Written by Luca
#Used for the display of game progress when setup
class GameDataLink:
    
    @staticmethod
    def init_data():
        return  {
            "earnedPoints" : 0,
            "neededPoints" : 45,
            "text" : "info about this game",
            "rewardText" : ""
        }

    @staticmethod
    def get_data():
        return json.loads(input())
    
    @staticmethod
    def send_data(gameData):
        print("<<"+json.dumps(gameData)+">>")