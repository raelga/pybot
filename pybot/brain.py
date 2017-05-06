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
                logger.warn("%s is confusing, skipping" % (memory_name))
                logger.error("%s: %s" % (memory_name, err))

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
        logger.error("%s: %s" % (action, err))


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


def remember(message):
    """Store messages somewhere."""
    logger.info("%s, %s, \"%s\", %s, \"%s\", \"%s\", \"%s\";",
                message.message_id,
                message.chat.chat_id, message.chat.chat_name,
                message.user.user_id, message.user.username,
                message.text, message.media)
