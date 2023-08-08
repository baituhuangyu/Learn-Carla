from DataSave import DataSave
from SynchronyModel import SynchronyModel
from config import cfg_from_yaml_file
from data_utils import objects_filter


def main():
    cfg = cfg_from_yaml_file("configs.yaml")
    model = SynchronyModel(cfg)
    dtsave = DataSave(cfg)
    try:
        model.set_synchrony()
        model.spawn_actors()
        model.set_actors_route()
        print("set_actors_route ok")
        model.spawn_agent()
        print("spawn_agent ok ")
        model.sensor_listen()
        step = 0
        STEP = cfg["SAVE_CONFIG"]["STEP"]
        model.world.tick()
        while True:
            if step > cfg["SAVE_CONFIG"]["TOTAL"]:
                break
            if step % STEP == 0:
                data = model.tick()
                data = objects_filter(data)
                dtsave.save_training_files(data)
                print(step / STEP)
            else:
                model.world.tick()
            step += 1
    finally:
        model.setting_recover()
        print("clean ok")


if __name__ == '__main__':
    main()
