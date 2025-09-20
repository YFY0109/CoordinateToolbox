from sympy import Reals, Expr, sympify

NumberExpr = int | float | Expr


def point_names():
    point_chars = [chr(i) for i in range(ord("A"), ord("A") + 26)]
    pouch = 0
    while True:
        for char in point_chars:
            if pouch == 0:
                yield char
            else:
                yield f"{char}_{pouch}"  # Latex syntax
        pouch += 1


class Point:
    exists_point_names = []

    def __init__(self, x: NumberExpr, y: NumberExpr, name: str = None):
        if name is None:
            for point_name in point_names():
                if point_name in self.exists_point_names:
                    continue
                break
            self.name = point_name  # noqa
            self.exists_point_names.append(point_name)
        else:
            if name in self.exists_point_names:
                raise ValueError(f"Point {name} already exists")
            else:
                self.name = name
                self.exists_point_names.append(name)

        if x not in Reals or y not in Reals:
            raise ValueError("Coordinates must be real numbers")

        if isinstance(x, Expr):
            self.x = x
        elif isinstance(x, (int, float)):
            self.x = sympify(x, rational=True)  # noqa
        if isinstance(y, Expr):
            self.y = y
        elif isinstance(y, (int, float)):
            self.y = sympify(y, rational=True)  # noqa

    def __repr__(self):
        return f"<Point {self.name}({self.x}, {self.y})>"

    def __str__(self):
        return f"{self.name}({self.x}, {self.y})"

    def change_name(self, new_name: str):
        if new_name in self.exists_point_names:
            raise ValueError(f"Point {new_name} already exists")
        else:
            self.exists_point_names.remove(self.name)
            self.name = new_name
            self.exists_point_names.append(new_name)

    def __delete__(self, instance):
        self.exists_point_names.remove(self.name)
        del self


class Line:
    def __init__(self, p1: Point = None, p2: Point = None, k: NumberExpr = None, b: NumberExpr = None):
        if not any([p1, p2, k, b]):
            raise ValueError("At least two points or slope and intercept must be provided")
        if any([p1, p2]) and any([k, b]):
            raise ValueError("Provide either two points or slope and intercept, not both")
        if any([p1, p2]) and not all([p1, p2]):
            raise ValueError("Both points must be provided")
        if p1 and p2:
            if p1 == p2:
                raise ValueError("Points must be different")
            if p1.x == p2.x:
                raise ValueError("Vertical lines are not supported")
            self.k = (p2.y - p1.y) / (p2.x - p1.x)  # slope
            self.b = p1.y - self.k * p1.x  # y-intercept
        # elif k is not None and b is not None:
