
class Node:
    def __init__(self, handlesEvents=False):
        self.position = (0, 0)
        self.rect_size = (64, 64)
        self.handlesEvents = handlesEvents
    
    def process(self, dp):
        print("add function to ", self)
    
    def on_event(self, e, engine):
        pass