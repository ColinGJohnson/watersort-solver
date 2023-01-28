from controller.WaterSortController import WaterSortController


def main():
    controller = WaterSortController('Pixel 7 Pro')
    print(controller.update_state())


if __name__ == "__main__":
    main()
