from Sim import *

DEBUG = False
resolution = (800, 600)


def main():
    simulator = Sim(resolution, DEBUG)
    simulator.loop()


main()
