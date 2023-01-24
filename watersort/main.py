import json


def main():
    with open("../resources/problems/problem1.json") as fp:
        initial = json.loads(fp.read())
        print("Problem:")
        print(initial)


if __name__ == "__main__":
    main()
