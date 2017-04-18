#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 brain.py       Wrapper to allow dynamic plug-in architecture in bots.
 Author:        Rael Garcia <self@rael.io>
 Date:          06/2016
 Usage:         Import the module to a bot.
 Tested on:     Python 3 / OS X 10.11.5
"""

import os
import time
import importlib
import logging
import threading
import queue

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

MEMORY_DIR = 'memory'


def memories():
    "Load python modules from memory folder"

    # Invalidates current cache
    importlib.invalidate_caches()

    # Path where the modules are stored
    memory_path = os.path.join(os.path.dirname(__file__), MEMORY_DIR)
    knowledge = list()

    # If the folder exists,  get the files
    if os.path.isdir(memory_path):
        memories = os.listdir(memory_path)
    else:
        logger.warn("%s missing, i'm useless :(" % memory_path)
        return knowledge

    # For each .py file, get name and load the module
    for memory in memories:

        if not memory.startswith("__") and memory.endswith(".py"):

            pypos = memory.find(".py")
            memory_name = memory[:pypos]

            try:
                memory = importlib.import_module(
                    "{}.{}.{}".format(__package__, MEMORY_DIR, memory_name))
                knowledge.append(importlib.reload(memory))
            except Exception as err:
                logger.error("%s is confusing, skipping" % (memory_name))
                logger.error("%s" % (err))

    return knowledge


def thougth(working_memory, knowledge, action, stimulus):
    "Thread oriented function, store return value on a queue"

    # Try to execute the 'action' method for each module
    try:
        method = getattr(knowledge, action, None)
        if callable(method):
            working_memory.put(method(stimulus))
    except Exception as err:
        logger.warn("%s not know how to %s" % (knowledge.__name__, action))
        logger.error("%s" % (err))


def process(action, input):
    "Execute the <action> on each module available in memories"

    thoughts = list()
    working_memory = queue.Queue()

    for knowledge in memories():
        thought = threading.Thread(target=thougth, args=(
            working_memory, knowledge, action, input))
        thoughts.append(thought)
        thought.start()

    for thought in thoughts:
        thought.join()

    output = list()

    while not working_memory.empty():
        output.append(working_memory.get())

    return list(filter(None, output))


def ears(words):
    """Call <hear> method on each module"""
    return process("hear", words)


def eyes(image):
    """Call <see> method on each module"""
    return process("see", image)


def interact(action, message):
    """Call <action> method on each module"""
    return process(action, message)


def remember(whoami, what, where, when, who):
    """Store messages somewhere."""
    logger.info("%s, %s, %s, %s,\"%s\";", whoami, what, where, when, who)


def choose(words):
    """Call choose action on each module"""
    return process("Pulsa para desplegar", words)


def menu(who):
    """Print main menu"""
    menu = [["Grupos", '_groups'],
            ["Battletags", '_battletags']]
    return menu


def submenu(words, who):
    """Print different submenus"""
    if words == '_groups':
        submenu = [
            ['Destiny', 'https://t.me/pkts_destiny'],
            ['Wildlands', 'https://t.me/joinchat/AAAAAD_ilo8nKdhZdQLm9Q'],
            ['Overwatch', 'https://t.me/pkts_overwatch'],
            ['Horizon', 'https://t.me/joinchat/AAAAAD-16s4VNcRaBxREnA'],
            ['Battlefield', 'https://t.me/pkts_battlefield'],
            ['Final Fantasy', 'https://t.me/joinchat/AzNL9D_0xS_0h6Q3H5m69Q'],
            ['GTA', 'https://t.me/joinchat/AzNL9ECAaKh4y3za3egFbw'],
            ['Space', 'https://t.me/joinchat/AzNL9EAy0gzR3etQ_Q4JSw'],
            ['Division', 'https://t.me/joinchat/ANSWpD4TPEtu5wGU6O7J3Q'],
            ['Souls', 'https://t.me/joinchat/AzNL9ACpL0yP02kER67Mhg'],
            ['Borderlands', 'https://t.me/joinchat/AzNL9AD3n5pKH_6e1trOZA'],
            ['Hearthstone', 'https://t.me/joinchat/AzNL9D7UHCsWDtfgz1cw3g'],
            ['PC Master Race', 'https://t.me/joinchat/AzNL9EFBO0e81gXlECiRzA'],
            ['Pokémon', 'https://t.me/joinchat/AzNL9D-KxgBdpa9RlWF2kg'],
            ['Nintendo', 'https://t.me/joinchat/AAAAAEE4x5M1gaboANV6aw'],
            ['StarWars', 'https://t.me/joinchat/AAAAAEBbCjW8vueDkXwFyQ'],
            ['Miscelánea', 'https://t.me/miscelanea'],
        ]
    else:
        submenu = [["Not implemented (yet)", 'home']]

    return submenu
