from engine import Engine, Actor

engine = Engine()
player = Actor("main Character", 200, 200)
#player.add_input()
engine.add_root(player)

engine.start()
