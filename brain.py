#!/usr/bin/env python
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

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def memories() :
    """Load python modules from memory folder"""

    # Invalidates current cache
    importlib.invalidate_caches()

    # Path where the modules are stored
    memory_path = "memory"
    knowledge = list()

    # If the folder exists, get the files
    if os.path.isdir(memory_path):
        memories = os.listdir(memory_path)
    else:
        logger.warn("%s missing, i'm useless :(" % memory_path)
        return knowledge

    # For each .py file, get name and load the module
    for memory in memories :
        if memory.find("__") == -1 and memory.find(".pyc") == -1 :
            pypos = memory.find(".py")
            memory_name = memory[:pypos]
            try:
                memory = importlib.import_module(memory_path + "." + memory_name)
                knowledge.append(importlib.reload(memory))
            except:
                logger.error("%s is confusing, skipping" % (memory_name))

    return knowledge

import queue

def thougth(working_memory, knowledge, action, input):
    """Thread oriented function, store return value on a queue"""
    # Try to execute the 'action' method for each module
    try:
        response = getattr(knowledge, action)(input)
        if response: working_memory.put(response)
    except:
        logger.warn("%s not know how to %s" % (knowledge.__name__, action))

def process(action, input) :
    """Execute the action on each module"""
    
    thoughts = list()
    working_memory = queue.Queue()

    for knowledge in memories() :
            thought = threading.Thread(target=thougth, args=(working_memory, knowledge, action, input))
            thoughts.append(thought)
            thought.start()

    for thought in thoughts:
        thought.join()

    output = list()

    while not working_memory.empty():
        output.append(working_memory.get())

    return output

def ears(words) :
    """Call hear action on each module"""
    return process("hear", words)

def eyes(words) :
    """Call hear action on each module"""
    return process("see", words)

def respond(words, stimulus):
    """Call hear action on each module"""
    return process(stimulus, words)

def choose(words) :
    """Call choose action on each module"""
    return process("choose", words)

def menu(who) :
    """Print main menu"""
    menu=[["Grupos", '_groups'], 
          ["PSN", '_psn'], 
          ["Battletags", '/batlletags']]
    return(menu)
	
def submenu(words, who) :
    """Print different submenus"""
    if words == '_groups':
        submenu=[['Destiny', 'https://telegram.me/pkts_destiny\''],
                    ['Overwatch', 'https://telegram.me/pkts_overwatch\''],
                    ['Battlefield', 'https://telegram.me/pkts_battlefield\''],
                    ['Final Fantasy', 'https://telegram.me/joinchat/AzNL9D_0xS_0h6Q3H5m69Q\''],
                    ['Grand Theft Auto', 'https://telegram.me/joinchat/AzNL9ECAaKh4y3za3egFbw\''],
                    ['Space Exploration', 'https://telegram.me/joinchat/AzNL9EAy0gzR3etQ_Q4JSw\''],
                    ['Division', 'https://telegram.me/joinchat/ANSWpD4TPEtu5wGU6O7J3Q\''],
                    ['Souls', 'https://telegram.me/joinchat/AzNL9ACpL0yP02kER67Mhg\''],
                    ['Borlderlands', 'https://telegram.me/joinchat/AzNL9AD3n5pKH_6e1trOZA\''],
                    ['Hearthstone', 'https://telegram.me/joinchat/AzNL9D7UHCsWDtfgz1cw3g\''],
                    ['PC Master Race', 'https://telegram.me/joinchat/AzNL9EFBO0e81gXlECiRzA\''],
                    ['PokÃ©mon', 'https://telegram.me/joinchat/AzNL9D-KxgBdpa9RlWF2kg\''],
                    ['MiscelÃ¡nea', 'https://telegram.me/miscelanea\'']]
    else:
        submenu=[["Sin opciones", 'nothing']]

    return(submenu)

def remember(when, where, who, what) :
    """Store messages somewhere."""
    logger.info("%s, %s, %s,\"%s\";" % (when, where, who, what))
