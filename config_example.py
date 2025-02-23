from engine_core import Engine, Object, Vector2D, World

class Engine(Engine):
    def start(self):
        world = World(40, 20, self)
        world.add_object(Object(Vector2D(20, 15), Vector2D(0, 0), 20))
        return world
