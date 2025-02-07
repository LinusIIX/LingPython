import pygame
from pygame.locals import *
import threading
import json
import subprocess
import shutil
import os

class Engine:
    def __init__(self):
        self.nodes = []
        self.running = True
        pygame.init()
        self.dp = pygame.display.set_mode((800, 800), pygame.HWSURFACE | pygame.DOUBLEBUF)
    
    def add_node(self, node):
        self.nodes.append(node)

    def run(self):
        while self.running:
            self.dp.fill((255, 255, 255))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                for node in self.nodes:
                    if node.handlesEvents:
                        node.on_event(e, self)
            for node in self.nodes:
                node.process(self.dp)
            pygame.display.flip()

    #def run_game(self, module):
    #    module.main({})

    def interact(self, caller):
        for node in self.nodes:
            if node != caller:
                if self.check_collision(node, caller):
                    print(node.moduleName, ":", node.modulePath)
                    assetsFolder = os.path.join(os.getcwd(), "assets")
                    curGameFolder = os.path.split(node.modulePath)[0]
                    localAssetFolder = os.path.join(curGameFolder, "assets")
                    shutil.copytree(assetsFolder, localAssetFolder, dirs_exist_ok=True)
                    process = subprocess.Popen(
                        ['python3', node.modulePath],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True  # Ensures input/output are handled as text (not bytes)
                    )
                    stdout, stderr = process.communicate(input=json.dumps(node.moduleData))
                    print(stdout, stderr)
                    if os.path.exists(localAssetFolder):
                        shutil.rmtree(localAssetFolder)
                    lastSIdx = stdout.rfind("<<") + 2
                    lastEIdx = stdout.rfind(">>")
                    node.moduleData = json.loads(stdout[lastSIdx:lastEIdx])


    def check_collision(self, node1, node2):
        """Checks if two nodes overlap based on position and rect_size."""
        x1, y1 = node1.position
        w1, h1 = node1.rect_size

        x2, y2 = node2.position
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
                    "modulePath" : os.path.join(root, 'main.py')
                })
        return main_files