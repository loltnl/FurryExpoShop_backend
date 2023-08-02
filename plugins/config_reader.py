import configparser

config = configparser.ConfigParser()
config.read("../configs/config.ini")

for i in config.items():
    print(i)