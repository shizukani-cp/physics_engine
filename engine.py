import time
import config

def main():
    engine = config.Engine()
    interval = 1 / engine.fps
    world = engine.start()

    while True:
        try:
            world._update(interval)
            world._render()

            if world._all_objects_out_of_bounds():
                engine.stop()
                break

            time.sleep(interval)
        except KeyboardInterrupt:
            engine.stop()
            break

if __name__ == "__main__":
    main()
