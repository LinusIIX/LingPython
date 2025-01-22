## Game Architecture


Game Engine - Overall scenario / main level
- Level {game state and object interface}
- Player {inputs and interactions}
- Interactions {objects and text}
 - Dor {open on completing minigames}
 - Stones {launch mini games}
|
v
Mini Games {returns game state???}


```
Game Engine
  loop -> game objects
  |    -> inputs -> game objects -> ...
   --> update game state
  |
   --> ...
```
Game Object
 interact(self : Actor)
 save() : Data
 update() : void
 is_updateable() : Bool

Actor
 hp : int
 inventory : Inventory
 effects : Effect[]
 interact(self : Actor)
 save() : Data
 update()

Inventory
 item : Item[]
 getItem() : Item
 addItem() : Item

GroundLayer
 groundLayers : GroundLayer[]
 pallet : GameObject[]
 layer : int[][]
 
