
#Underlying base structure
#Writen by Luca
class Node:
    def __init__(self, handlesEvents=False, nodeRefs = {}, callProcess=True):
        self.position = (0, 0)
        self.offsetPos = (0, 0)  #So that the camera "follows" the player
        self.rect_size = (0, 0)
        self.handlesEvents = handlesEvents
        self.callProcess = callProcess #Determines if process function gets called
        self.runnable = False
        self.children = []
        self.nodeRefs = nodeRefs
        self.interactable = False
    
    #Gets called every "cycle" of engine
    def process(self, dp):
        print("add function to ", self)
    
    #Gets called if interacted with
    def on_event(self, e, engine):
        pass
    
    #So that you can make Tree structures
    def add_node(self, node):
        self.children.append(node)
    
    def remove_node(self, node):
        self.children.remove(node)
    
    #helper functions to work with offset:

    def setPos(self, x, y):
        self.position = (x, y)
        self.update_offset()

    def update_offset(self):
        for node in self.children:
            node.offsetPos = self.getPos()
            node.update_offset()

    def getPos(self):
        return (self.getX(), self.getY())

    def getX(self):
        return self.position[0] + self.offsetPos[0]
    
    def getY(self):
        return self.position[1] + self.offsetPos[1]