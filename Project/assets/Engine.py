import pygame
from pygame.locals import *
import json
import subprocess
import shutil
import os
import sys
import multiprocessing
from assets import Node, globals
#The Underlying Engine that goes trough all the
#Written by mostly Luca and a bit Linus
class Engine:
    def __init__(self, width=800, height=800):
        self.nodes = []
        self.running = True
        pygame.init()
        self.dp = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    
    #Same as in "node" to allow a Tree structure and to give itself the elements to run trough
    def add_node(self, node):
        self.nodes.append(node)
    #The function to start the gameloop
    def run(self):
        try:
            while self.running: #The main gameloop
                self.dp.fill((255, 255, 255))
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.running = False
                    for node in self.nodes:
                        if node.handlesEvents:
                            node.on_event(e, self)
                nodeStack = self.nodes.copy() #goes trough every node attached to itself
                while len(nodeStack) > 0:
                    node = nodeStack.pop(0)
                    if globals.debug: #debug
                        pygame.draw.rect(self.dp, (200, 10, 10), ((node.getX(), node.getY()), node.rect_size), 15)
                        if node.interactable:
                            pass
                            #print(node.getPos())
                    if node.callProcess:
                        node.process(self.dp) #Calls the process function in all nodes that use it
                    nodeStack = node.children + nodeStack #Add children after their parent node
                pygame.display.flip()
        except KeyboardInterrupt:
            print("  goodbye  ")
            exit()
    
    #To start console games
    def run_console(self, node):
        global_vars = {}
        print("||| Running game in console | exit with Ctrl C |||")
        try:
            exec(open(node.modulePath).read(), global_vars)
        except KeyboardInterrupt:
            print("\n\nexiting console game")


    #To start pygame games
    def run_game(self, node):
        #Get all the folders and access them
        mainFolder = os.getcwd()
        assetsFolder = os.path.join(mainFolder, "assets")
        curGameFolder = os.path.split(node.modulePath)[0]
        localAssetFolder = os.path.join(curGameFolder, "assets")
        if node.hasInterface:
            shutil.copytree(assetsFolder, localAssetFolder, dirs_exist_ok=True) #gets the interface
        os.chdir(curGameFolder)
        #Start the game
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Ensures input/output are handled as text (not bytes)
        )

        stdout, stderr = process.communicate(input=json.dumps(node.moduleData))
        os.chdir(mainFolder)
        if globals.debug:
            print(stdout, stderr)
        #Does not work on windows TODO no need as still works
        #if os.path.exists(localAssetFolder):
        #    shutil.rmtree(localAssetFolder)
        lastSIdx = stdout.rfind("<<") + 2
        lastEIdx = stdout.rfind(">>")
        #To display ingame(in ours)
        if (min(lastSIdx, lastEIdx) >= 0):
            node.moduleData = json.loads(stdout[lastSIdx:lastEIdx])
            newPointsInfo = "| " + str( node.moduleData["earnedPoints"]) + "/" + str(node.moduleData["neededPoints"])
            node.description = node.description.replace(node.pointsInfo, newPointsInfo)
        else:
            print("/(!)\\ game data not send, (or project crash)")

    #gets called if the player presses interact key
    def interact(self, caller):
        nodeStack = self.nodes.copy()#checks every node if it can be interacted with
        while len(nodeStack) > 0:
            node = nodeStack.pop(0)
            if node != caller:
                if self.check_collision(node.getPos(), node.rect_size, caller):#something can be interacted with if it collides with the player
                    if globals.debug:
                        #print(node.moduleName, ":", node.modulePath)
                        pass
                    if node.interactable:
                        node.interact(caller)#if it is something interactable that isn't a minigame call 
                    if node.runnable:
                        if node.consoleRun == True:
                            self.run_console(node)
                        else:
                            if node.description.find("frog") != -1 and caller.holding == "nothing":#so that the frog game can only be played with net
                                pass
                            else:
                                if node.modulePath != "":
                                    self.run_game(node)
            nodeStack = node.children + nodeStack #Add children after their parent node


    @staticmethod
    def load_sprite_sheet(sheet, frame_width, frame_height, num_frames, size=globals.game_size):
        frames = []
        #Cuts up the Spritesheet up and adds it to frames
        for i in range(num_frames):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame_rect = frame.get_rect()
            frame = pygame.transform.scale(frame, (size * frame_rect.width, size * frame_rect.height))
            frames.append(frame)
        return frames

    #checks collision
    @staticmethod
    def check_collision(pos, rect_size, node2):
        """Checks if two nodes overlap based on position and rect_size."""
        x1, y1 = pos
        w1, h1 = rect_size

        x2, y2 = node2.getX(), node2.getY()
        w2, h2 = node2.rect_size

        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)
