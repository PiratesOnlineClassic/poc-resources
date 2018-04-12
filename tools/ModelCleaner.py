import __builtin__,sys,imp,os,time,stat,string,re,getopt,fnmatch,threading,signal,shutil,platform,glob,getpass,signal,subprocess
from panda3d.core import *
from direct.showbase import Loader, ShowBase

__builtins__['base'] = ShowBase.ShowBase()

__builtins__['loader'] = Loader.Loader(base)

SOURCE_ROOT = os.path.dirname(os.path.abspath(__file__))

phaseNames = ['phase_2', 'phase_3', 'phase_4', 'phase_5']

loadPrcFileData('', 'vfs-mount phase_2 phase_2')
loadPrcFileData('', 'vfs-mount phase_3 phase_3')
loadPrcFileData('', 'vfs-mount phase_4 phase_4')
loadPrcFileData('', 'vfs-mount phase_5 phase_5')

loadPrcFileData('', 'bam-texture-mode relative')
loadPrcFileData('', 'egg-texture-mode relative')
loadPrcFileData('', 'egg-combine-geoms 1')
loadPrcFileData('', 'flatten-collision-nodes 1')

print "Cleaned models will be output into the 'cleaned' directory. This directory is ignored by Git via .gitignore.\n"
print "Don't forget to move CleanModels.bat and ModelCleaner.py back to the tools folder after you're done!\n"

class ModelCleaner:
    def __init__(self):
        self.files = []
        self.outFiles = []

    def _recurse_dir(self, dir):
        for f in os.listdir(dir):
            fDS = f
            f = os.path.join(dir, f)

            if os.path.isdir(f):
                self._recurse_dir(f) 
            elif not f.endswith('bam'):
                continue
            elif f.endswith('bam'):
                self.files.append(str(f))
            else:
                continue
        
    def process_modules(self):
        for file in self.files:
            try:
                model = loader.loadModel(file)
                model.clearModelNodes()	
                model.flattenStrong()
                model.forceRecomputeBounds()
            except:
                continue
            
            file = os.path.join("cleaned\\", file)
            
            file = str(file)
            
            directory = os.path.dirname(file)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            if not os.path.exists(file):
                open(file, 'w+').close()
                
            path = Filename(file)
            #print path.getFullpath()
            path.setBinary()
            #success = model.writeBamFile(path)
            success = loader.saveModel(path, model)
            
            if not success:
                print "Oh no! The model write failed!\n"
            
cleaner = ModelCleaner()
for name in phaseNames:
    cleaner._recurse_dir(name)
cleaner.process_modules()