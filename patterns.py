class Singleton(object):
    __instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_.__instance, class_):
            class_.__instance = object.__new__(class_, *args, **kwargs)
        return class_.__instance

print('-'*20 + ' SINGLETON ' + '-'*20)
a = Singleton()
print(id(a))
b = Singleton()
print(id(b))


class WoodenBrigade:
    
    def build_wall(self):
        print('Built a wall using wood')

    def build_roof(self):
        print('Built a roof with windows')


class IronBrigade:
    
    def build_wall(self):
        print('Built a wall using iron')

    def build_roof(self):
        print('Built a roof without windows')


class BuildingCompany:

    def __init__(self, brigade):
        self.brigade = brigade

    def build_basement(self):
        print('Built basement')

    def build_wall(self):
        self.brigade.build_wall()

    def build_roof(self):
        self.brigade.build_roof()

    def build_house(self):
        self.build_basement()
        self.build_wall()
        self.build_roof()


print('-'*20 + ' BRIDGE ' + '-'*20)
wooden_brigade = WoodenBrigade()
iron_brigade = IronBrigade()
company = BuildingCompany(wooden_brigade)
company.build_house()
company.brigade = iron_brigade
company.build_house()


print('-'*20 + ' OBSERVER ' + '-'*20)

class Parent:

    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"[{self.name}] observer received message: {message}")


class Child:
    def __init__(self):
        self.observers = []
    
    def attach(self, observer):
        self.observers.append(observer)
    
    def detach(self, observer):
        self.observers.remove(observer)
    
    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


class Pupil(Child):
    def __init__(self):
        super().__init__()
        self.mark = None
    
    def set_mark(self, mark):
        self.mark = mark
        self.notify(mark)


pupil = Pupil()
observer1 = Parent('Father')
observer2 = Parent('Mother')
pupil.attach(observer1)
pupil.attach(observer2)
pupil.set_mark(10)
pupil.detach(observer2)
pupil.set_mark(5)