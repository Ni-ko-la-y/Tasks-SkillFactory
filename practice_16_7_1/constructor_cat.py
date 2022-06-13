class Cat:
    list_cats = []
    def __init__(self, name, gender, age=None):
        self.name = name
        self.gender = gender
        self.age = age

    def data(self):
        if True:
            Cat.list_cats.append(self)

    def info():
        for obj in Cat.list_cats:
            print(f"Кличка питомца - {obj.name}"
                  f" | Пол - {obj.gender}"
                  f" | Возраст - {obj.age}")
