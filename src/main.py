from src.Sim import Sim

DEBUG = True
resolution = (800, 600)


def main():
    simulator = Sim(resolution, DEBUG)
    simulator.loop()


main()
