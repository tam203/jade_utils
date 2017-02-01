import s3fs
import re
import os

class Loader:
    def __init__(self):
        self.local_path = '/usr/local/share/notebooks/data'
        self.fs = s3fs.S3FileSystem()
        
    def list_buckets(self):
        return os.listdir(self.local_path)
    
    def list_files(self, dirpath):
        return [self.local_path + '/' + path for path in self._list_files(dirpath)]
    
    def _list_files(self, dirpath):
        if len(self.fs.ls(dirpath)) == 0:
            return []
        elif self.fs.ls(dirpath, True)[0]['StorageClass'] == 'DIRECTORY':
            # recurse
            child_lists = [self._list_files(child) for child in self.fs.ls(dirpath)]
            return [f for c in child_lists for f in c] # iterate through all child directories
        else:
            files = self.fs.glob(dirpath+'/*')
            return files