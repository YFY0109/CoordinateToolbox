from sympy import Reals, Expr

NumberExpr = int | float | Expr

def point_names():
    point_chars = [chr(i) for i in range(ord("A"), ord("A") + 26)]
    pouch = 0
    while True:
        for char in point_chars:
            if pouch == 0:
                yield char
            else:
                yield f"{char}_{pouch}" # Latex syntax
        pouch += 1

class Point:
    exists_point_names = []
    def __init__(self, x: NumberExpr, y: NumberExpr, name: str = None):
        if name is None:
            for point_name in point_names():
                if point_name in self.exists_point_names:
                    continue
                break
            self.name = point_name # noqa

        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point = None, p2: Point = None):
        self.p1 = p1
        self.p2 = p2