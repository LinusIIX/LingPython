
class Node:
    def __init__(self, handlesEvents=False, nodeRefs = {}, callProcess=True):
        self.position = (0, 0)
        self.offsetPos = (0, 0)
        self.rect_size = (0, 0)
        self.handlesEvents = handlesEvents
        self.callProcess = callProcess
        self.runnable = False
        self.children = []
        self.nodeRefs = nodeRefs
        self.interactable = False
    
    def process(self, dp):
        print("add function to ", self)
    
    def on_event(self, e, engine):
        pass
    
    def add_node(self, node):
        self.children.append(node)
    
    def remove_node(self, node):
        self.children.remove(node)
    
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