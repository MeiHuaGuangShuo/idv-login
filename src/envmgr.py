# coding=UTF-8
class genv:
    _dict = {}
    
    @classmethod
    def set(cls, key, value):
        cls._dict[key] = value
    
    @classmethod
    def get(cls, key, default = None):
        if key in cls._dict:
            return cls._dict[key]
        return default

    def __setitem__(self, key, value):
        self._dict[key] = value

    def __getitem__(self, key):
        return self._dict[key]
