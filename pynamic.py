from pickle import (load, dump)
from os import listdir

class pynamic(object):
    def __init__(self, save_directory):
        self.save_directory = save_directory
    
    def __call__(self, f):
        cache = {}
        
        def wrapper(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]
        
        warpper.cache = cache
        return wrapper
