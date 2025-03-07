from assets import Engine, Node, GameDataLink, Player, BackGround, EventStone, TextDisplay, globals


engine = Engine()
root = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
engine.add_node(root)

backGround = BackGround() #position ist startposition
root.add_node(backGround)

i = 100
eventStoneDescriptions = ["hello", "wow sagsfdajgkk k sdg sfkgksfd kgsfdk gpos kdg", "cool"]
eventStoneContainer = Node(handlesEvents=False, nodeRefs={}, callProcess=False)
root.add_node(eventStoneContainer)
for gameEntry, gameDescriptions in zip(Engine.get_main_files("games"), eventStoneDescriptions):
    if globals.debug:
        print(gameEntry, gameDescriptions)
    eventStoneContainer.add_node(EventStone(gameEntry, gameDescriptions, (0, i)))
    i += 100

player = Player(handlesEvents=True, nodeRefs={
    "root" : root,
    "bg"   : backGround
})
player.rect_size = (player.sprite_rect.width,player.sprite_rect.height)
engine.add_node(player)

playerUI = TextDisplay(handlesEvents=False, nodeRefs={"player" : player, "eventStoneContainer" : eventStoneContainer})
root.add_node(playerUI)

engine.run()