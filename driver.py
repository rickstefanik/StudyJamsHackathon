#! /usr/bin/env python3

from MelodyController import MelodyController

if __name__ == "__main__":
    mc = MelodyController()
    mc.watsonSpeak("I am doing this from a driver class", 0)
