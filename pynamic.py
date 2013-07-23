#!/usr/bin/python
"""
Pynamic is a module for caching the result of very expensive computations
to disk.

Pynamic works on the function level as a decorator. It uses the fact that a 
function and its arguments are objects and will hash them together to create 
a unique file name. A pickle file is then created with the results of the
computation. The next time the same function is called with the same 
arguments, the pickle file will be loaded instead of running the function.
"""
from pickle import load, dump
from os import listdir, makedirs
from os.path import isfile, exists
from shutil import rmtree

class pynamic(object):
    _suffix = '.pickle'
    save_directory_default = '.'

    def __init__(self, f, save_directory=None, function_name=None, version=None, input_name=None):
        """ Called on decorated function at definition time. Instead of 
        relying on function and argument hashing, it allows you to define 
        a function name, function version, and/or input identifier. Note that 
        specifying a function name AND input name will cause the function to 
        only run once, and to load a pickle file any other time it is called. 
        """
        self.f = f 
        self.save_directory = save_directory
        self.function_name = function_name if function_name else f.__name__
        self.version = version if version else ''
        self.input_name = input_name
        
        if save_directory is None:
            self.save_directory = self.save_directory_default
        
        if not exists(self.save_directory):
            makedirs(self.save_directory)
        
        suf_len = len(self._suffix)
        self.cache = [f[:-suf_len] for f in listdir(self.save_directory) if isfile(f) and f[-suf_len:] == self._suffix]
    
    def __call__(self, *args, **kwargs):
        i = self.input_name if self.input_name else (args, str(kwargs))
        v = self.version
        fn = self.function_name
        
        uniquekey = str(abs(hash((i, v, fn))))
        
        if uniquekey in self.cache:
            print 'Using cached result for', self.f.__name__
            with open(self.save_directory + '/' + uniquekey + self._suffix, 'r') as result_file:
                result = load(result_file)
        else:
            print 'Caching output from', self.f.__name__
            with open(self.save_directory + '/' + uniquekey + self._suffix, 'w') as result_file:
                result = self.f(*args, **kwargs)
                dump(result, result_file)
                self.cache.append(uniquekey)
        return result
                
if __name__ == "__main__":
    """ Run a series of tests on this module """
    
    # Automatic function and input hashing
    pynamic.save_directory_default = 'test_cache'
    
    @pynamic
    def myfunction(a, k='default kwarg'):
        return 'running myfunction', a, k
        
    @pynamic
    def myfunction2(b):
        return 'running myfunction2', b
    
    print myfunction(1, 7)
    print myfunction(1, 8)
    print myfunction(1, 7)
    
    print myfunction2(17)

    rmtree(pynamic.save_directory_default)
