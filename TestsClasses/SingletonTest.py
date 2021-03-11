"""This class is just a test of the singleton implementation in python"""

class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def some_buisness_logic(self):
        print("test")

    def set_val(self, val):
        self.val = val

if __name__ == "__main__":
    s1 = Singleton()
    s1.set_val("abc")
    s2 = Singleton()
    print(s2.val)

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
