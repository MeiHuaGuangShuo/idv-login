# coding=UTF-8
import json
import os


class genv:
    _dict = {}
    _cachePath = "config.json"

    @classmethod
    def set(cls, key, value, cached=False):
        cls._dict[key] = value
        if isinstance(value, (str, int, float, bool, list, dict)) and isinstance(key, str):
            if cached:
                try:
                    if os.path.exists(cls._cachePath):
                        with open(cls._cachePath, 'r') as f:
                            data = json.load(f)
                    else:
                        data = {}
                    data[key] = value
                    with open(cls._cachePath, 'w') as f:
                        json.dump(data, f)
                except:
                    print("Failed to cache data", key, value)
                    pass

    @classmethod
    def get(cls, key, default=None):
        if key in cls._dict:
            return cls._dict[key]
        else:
            try:
                with open(cls._cachePath, 'r') as f:
                    data = json.load(f)
                    if key in data:
                        return data[key]
                    else:
                        return default
            except:
                return default

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]
