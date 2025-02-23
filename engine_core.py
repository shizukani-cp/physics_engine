import os

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

class UnGravitibleObject:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def update(self, world, dt):
        self.position += self.velocity * dt
        if self.position.y < 0:
            self.position.y = 0
            self.velocity.y *= -world.config.repulsion

class GravitibleObject(UnGravitibleObject):
    def update(self, world, dt):
        self.velocity += Vector2D(0, -world.config.gravity) * dt
        print(self.velocity.x, self.velocity.y)
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
        self.config.after_update(self)

    def _render(self):
        self._clear_console()
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        for obj in self.objects:
            x = int(obj.position.x)
            y = int(self.height - obj.position.y - 1)
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = 'O'

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

