from json import load, dump


class Config:

    def __init__(self, filename, default_values: list = {}):
        self.__filename__ = filename

        for key, value in default_values.items():
            self.__dict__[key] = value

        try:
            with open("data/{}.json".format(filename)) as file:
                self.__dict__.update(load(file))
        except FileNotFoundError:
            with open("data/{}.json".format(filename), "w") as file:
                file.write("{}")

    def save(self):
        __dict__ = {key: item for key, item in self.__dict__.items()
                    if key != "__filename__"}
        with open("data/{}.json".format(self.__filename__), "w") as file:
            dump(__dict__, file)
