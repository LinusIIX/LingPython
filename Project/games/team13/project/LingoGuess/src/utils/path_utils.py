# path_utils.py
# Author: Max Weber
# if you want to see more detailed information about the individual contributors of the code files, 
# please have a look at the "contributors.txt" file (in the "project" directory)

import os
import sys
from pathlib import Path

class PathUtils:
    _instance = None
    _base_path = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PathUtils, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the base path by finding the git repository root"""
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # Traverse up until we find the git repository root or hit the filesystem root
        while current_dir != current_dir.parent:
            if (current_dir / '.git').exists():
                self._base_path = current_dir / 'project'
                break
            if (current_dir / 'project').exists():
                self._base_path = current_dir / 'project'
                break
            current_dir = current_dir.parent
        
        if self._base_path is None:
            raise RuntimeError("Could not find project root directory")
        
        # Add src directory to Python path
        src_path = self._base_path / 'LingoGuess' / 'src'
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))
    
    @property
    def base_path(self):
        """Get the base path of the project"""
        return self._base_path
    
    def get_resource_path(self, *paths):
        """Get the absolute path for a resource within the project"""
        return os.path.join(self._base_path, 'LingoGuess', 'src', *paths)
    
    def get_image_path(self, image_name):
        """Get the absolute path for an image resource"""
        return self.get_resource_path('photographics', image_name) 