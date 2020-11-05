class Point(tuple):
    def __new__(cls, x, y):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return self.__getitem__(0)

    @property
    def y(self):
        return self.__getitem__(1)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"Point{tuple.__repr__(self)}"
