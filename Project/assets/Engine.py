import pygame
from pygame.locals import *
import json
import subprocess
import shutil
import os
import sys
import multiprocessing
from assets import Node, globals


class Engine:
    def __init__(self, width=800, height=800):
        self.nodes = []
        self.running = True
        pygame.init()
        self.dp = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
    
    def add_node(self, node):
        self.nodes.append(node)

    def run(self):
        try:
            while self.running:
                self.dp.fill((255, 255, 255))
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.running = False
                    for node in self.nodes:
                        if node.handlesEvents:
                            node.on_event(e, self)
                nodeStack = self.nodes.copy()
                while len(nodeStack) > 0:
                    node = nodeStack.pop(0)
                    if globals.debug: #debug
                        pygame.draw.rect(self.dp, (200, 10, 10), ((node.getX(), node.getY()), node.rect_size), 15)
                    if node.callProcess:
                        node.process(self.dp)
                    nodeStack = node.children + nodeStack #Add children after their parent node
                pygame.display.flip()
        except KeyboardInterrupt:
            print("  goodbye  ")
            exit()
    
    def run_console(self, node):
        global_vars = {}
        print("||| Running game in console | exit with Ctrl C |||")
        try:
            exec(open(node.modulePath).read(), global_vars)
        except KeyboardInterrupt:
            print("\n\nexiting console game")



    def run_game(self, node):
        mainFolder = os.getcwd()
        assetsFolder = os.path.join(mainFolder, "assets")
        curGameFolder = os.path.split(node.modulePath)[0]
        localAssetFolder = os.path.join(curGameFolder, "assets")
        shutil.copytree(assetsFolder, localAssetFolder, dirs_exist_ok=True)
        os.chdir(curGameFolder)
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
        if (min(lastSIdx, lastEIdx) >= 0):
            node.moduleData = json.loads(stdout[lastSIdx:lastEIdx])
        else:
            print("/(!)\\ game data not send, (or project crash)")


    def interact(self, caller):
        nodeStack = self.nodes.copy()
        while len(nodeStack) > 0:
            node = nodeStack.pop(0)
            if node != caller:
                if self.check_collision(node.getPos(), node.rect_size, caller):
                    if globals.debug:
                        print(node.moduleName, ":", node.modulePath)
                    if node.consoleRun == True:
                        self.run_console(node)
                        #self.codeProcess = multiprocessing.Process(target=self.run_console, args=(node, ))
                        #self.codeProcess.start()
                        #self.codeProcess.join()
                    else:
                        self.run_game(node)
            nodeStack = node.children + nodeStack #Add children after their parent node


    @staticmethod
    def load_sprite_sheet(sheet, frame_width, frame_height, num_frames):
        frames = []
        for i in range(num_frames):
            frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            frame_rect = frame.get_rect()
            frame = pygame.transform.scale(frame, (globals.game_size * frame_rect.width, globals.game_size * frame_rect.height))
            frames.append(frame)
        return frames


    @staticmethod
    def check_collision(pos, rect_size, node2):
        """Checks if two nodes overlap based on position and rect_size."""
        x1, y1 = pos
        w1, h1 = rect_size

        x2, y2 = node2.getX(), node2.getY()
        w2, h2 = node2.rect_size

        return (x1 < x2 + w2 and x1 + w1 > x2 and
                y1 < y2 + h2 and y1 + h1 > y2)


    @staticmethod
    def get_main_files(base_path):
        main_files = []
        for root, dirs, files in os.walk(base_path):  # Walk through all folders
            if 'main.py' in files:  # Check if 'main.py' exists in the current folder
                main_files.append({
                    "moduleFolderName" : os.path.basename(root),
                    "modulePath" : os.path.join(root, 'main.py'),
                    "consoleRun" : False
                })
            if 'main_console.py' in files:
                main_files.append({
                    "moduleFolderName" : os.path.basename(root),
                    "modulePath" : os.path.join(root, 'main_console.py'),
                    "consoleRun" : True
                })
        return main_files