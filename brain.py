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

def remember(when, where, who, what) :
    """Store messages somewhere."""
    logger.info("%s, %s, %s,\"%s\";" % (when, where, who, what)) 
