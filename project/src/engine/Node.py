class Node:

    #def __init__(self, hasProcess, isIntractable, imgName, position = (0,0), rectWidth = (0,0), scriptName=None, animSlots=None, animSubdivs=None, curImgIdx=None):
    def __init__(self):
        pass
        # self.hasProcess = hasProcess
        # self.isIntractable = isIntractable
        # self.position = position
        # self.rectWidth = rectWidth
        # self.attachedScript = scriptName
        # self.attachedImage = imgName
        # self.animSlots = animSlots
        # self.animSubdivs = animSubdivs
        # self.curImgIdx = curImgIdx
        # if scriptName:
        #     self.script = __import__(self.attachedScript)
    
    def process(self, display):
        self.script.process(display)