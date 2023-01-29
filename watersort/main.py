from pprint import pprint

from controller.WaterSortController import WaterSortController


def main():
    controller = WaterSortController('Pixel 7 Pro')
    pprint(controller.update_state())


if __name__ == "__main__":
    main()
