import os

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

class UnGravitibleObject:
    def __init__(self, position, char="O"):
        self.position = position
        self.char = char

    def update(self, world, dt):
        pass

class GravitibleObject(UnGravitibleObject):
    def __init__(self, position, velocity, mass, char="O"):
        super().__init__(position)
        self.velocity = velocity
        self.mass = mass

    def update(self, world, dt):
        self.velocity += Vector2D(0, -world.config.gravity) * dt
        self.position += self.velocity * dt
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -world.config.repulsion
        super().update(world, dt)

class Object(GravitibleObject):
    pass

class World:
    def __init__(self, width, height, config):
        self.width = width
        self.height = height
        self.config = config
        self.frame_num = 0
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def _update(self, dt):
        self.config.before_update(self)
        for obj in self.objects:
            obj.update(self, dt)
        self.frame_num += 1
        self.check_collisions()
        self.config.after_update(self)

    def check_collisions(self):
        for i in range(len(self.objects)):
            for j in range(i + 1, len(self.objects)):
                obj1 = self.objects[i]
                obj2 = self.objects[j]
                if (int(obj1.position.x) == int(obj2.position.x) and
                    int(obj1.position.y) == int(obj2.position.y)):
                    if type(obj1) is type(obj2) and type(obj1) in (GravitibleObject, Object):
                        self.resolve_collision(obj1, obj2)
                    else:
                        if isinstance(obj1, UnGravitibleObject):
                            obj1, obj2 = obj2, obj1
                        obj1.position.y = obj2.position.y + 1
                        obj1.velocity.y *= -self.config.repulsion

    def resolve_collision(self, obj1, obj2):
        total_mass = obj1.mass + obj2.mass
        v1 = ((obj1.mass - obj2.mass) * obj1.velocity + 2 * obj2.mass * obj2.velocity) / total_mass
        v2 = ((obj2.mass - obj1.mass) * obj2.velocity + 2 * obj1.mass * obj1.velocity) / total_mass
        obj1.velocity = v1
        obj2.velocity = v2

    def _render(self):
        self._clear_console()
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        for obj in self.objects:
            x = int(obj.position.x)
            y = int(self.height - obj.position.y - 1)
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = obj.char

        for row in grid:
            print(''.join(row))
        print('-' * self.width)

    def _clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _all_objects_out_of_bounds(self):
        for obj in self.objects:
            if (0 <= obj.position.x < self.width and
                0 <= obj.position.y < self.height):
                return False
        return True


class Engine:

    fps = 10
    gravity = 9.8
    repulsion = 0.8

    def start(self):
        return World(40, 20, self)

    def before_update(self, world):
        pass

    def after_update(self, world):
        pass

    def stop(self):
        print("シミュレーションを終了します。")

