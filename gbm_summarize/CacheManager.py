#!/usr/bin/env python3
'''
CacheManager
Simple cache manager for storing returned API data
    in a flat file for subsequent calls
'''
import json

class CacheManager:
    def __init__(self, file=None):
        # Set the file path/name
        self.file = file

        try:
            # Try to read the file
            with open(self.file, 'r') as cache_file:
                self.cache = json.load(cache_file)
        except EnvironmentError:
            # IOError or OSError, file not found
            self.cache = {}

    def fetch(self, key=''):
        # Return cache key if it exists
        return self.cache.get(key)

    def update(self, key='', value=''):
        # Update cache
        if key and value:
            # Append new key/val to local file
            self.cache.update(
                {key: value}
            )
            # Write it on out
            try:
                with open(self.file, 'w') as o:
                    json.dump(self.cache, o)
            except EnvironmentError:
                print('Unable to write to cache file!')
