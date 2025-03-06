
class Node:
    def __init__(self, handlesEvents=False, nodeRefs = {}, callProcess=True):
        self.position = (0, 0)
        self.offsetPos = (0, 0)
        self.rect_size = (0, 0)
        self.handlesEvents = handlesEvents
        self.callProcess = callProcess
        self.children = []
        self.nodeRefs = nodeRefs
    
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
            node.offsetPos = (self.getX(), self.getY())
            node.update_offset()


    def getX(self):
        return self.position[0] + self.offsetPos[0]
    
    def getY(self):
        return self.position[1] + self.offsetPos[1]