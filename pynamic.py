#!/usr/bin/python

from pickle import load, dump
from os import listdir
from os.path import isfile

class pynamic(object):
    suffix = '.cache'

    def __init__(self, f, save_directory='.', function_name=None, version=None, input_name=None):
        self.f = f 
        self.save_directory = save_directory
        self.function_name = function_name if function_name else f.__name__
        self.version = version if version else ''
        self.input_name = input_name
        
        suf_len = len(self.suffix)
        self.cache = [f[:-suf_len] for f in listdir(self.save_directory) if isfile(f) and f[-suf_len:] == self.suffix]
    
    def __call__(self, *args, **kwargs):
        i = self.input_name if self.input_name else (args, str(kwargs))
        v = self.version
        fn = self.function_name
        
        uniquekey = str(abs(hash((i, v, fn))))
        
        if uniquekey in self.cache:
            print 'found in cache'
            with open(uniquekey + self.suffix, 'r') as result_file:
                result = load(result_file)
        else:
            print 'new to cache'
            with open(uniquekey + self.suffix, 'w') as result_file:
                result = self.f(*args, **kwargs)
                dump(result, result_file)
                self.cache.append(uniquekey)
        return result
                
if __name__ == "__main__":
    @pynamic
    def myfunction(a, k='default kwarg'):
        return 'running myfunction', a, k
    
    print myfunction(1, 7)
    
    # TODO:
    # Allow for raw file name to be specified as well
    # See if file name can be made in parts with "short" hashes
