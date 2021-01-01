# import pickle
#
#
# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]
#
#
# class Caches(metaclass=Singleton):
#
#     def __init__(self):
#         self.caches = dict()
#         self.i = 0
#
#     def get_cache(self):
#         instance = Cache()
#         self.caches[self.i] = instance
#         self.i += 1
#         return instance
#
#     def save_cache(self, path: str):
#         for cache in self.caches:
#             with open(path + str(cache), 'wb') as f:
#                 pickle.dump(self.caches[cache], f)
#
#     def load_cache(self, path: str):
#         with open(path, 'rb') as f:
#             json_in = pickle.load(f)
#             self.caches = json_in
#
#
# class Cache:
#     def __init__(self):
#         self.instance = dict()
#
#     def set(self, key, value):
#         self.instance[key] = value
#
#     def get(self, key):
#         return self.instance[key]



