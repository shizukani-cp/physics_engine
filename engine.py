import time
import config

def main():
    engine = config.Engine()
    interval = 1 / engine.fps
    world = engine.start()

    while True:
        world._update(interval)
        world._render()

        if world._all_objects_out_of_bounds():
            print("すべてのオブジェクトが画面外に出ました。シミュレーションを終了します。")
            break

        time.sleep(interval)

if __name__ == "__main__":
    main()
