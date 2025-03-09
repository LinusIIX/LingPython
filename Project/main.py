import json
from assets import Engine, Node, GameDataLink, Player, BackGround, EventStone, TextDisplay, globals


engine = Engine()
root = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
engine.add_node(root)

eventStoneContainer = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
player = Player(handlesEvents=True)
backGround = BackGround((650, 600), nodeRefs= {
    "player" : player,
    #"eventStoneContainer" : eventStoneContainer
})
eventStoneContainer.position = backGround.position
root.add_node(backGround)
root.setPos(player.position[0],player.position[1])
i = 100
eventStoneDescriptions = ["hello", "wow sagsfdajgkk k sdg sfkgksfd kgsfdk gpos kdg", "cool"]
eventStoneData = json.loads(open("eventStoneData.json").read())
#eventStoneContainer.re
root.add_node(eventStoneContainer)
for data in eventStoneData:
    eventStoneContainer.add_node(EventStone(data["module"], data["description"], data["position"], data["rect_size"]))
    i += 100

player.nodeRefs = {
    "root" : root,
    "bg"   : backGround,
    #"eventStoneContainer" : eventStoneContainer
}
player.rect_size = (player.sprite_rect.width,player.sprite_rect.height)
engine.add_node(player)

playerUI = TextDisplay(handlesEvents=False, nodeRefs={"player" : player, "eventStoneContainer" : eventStoneContainer})
root.add_node(playerUI)

engine.run()