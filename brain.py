#!/usr/bin/env python

import os
import time
import importlib

import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def memories() :

    importlib.invalidate_caches()
    
    memory_path = "memory"
    knowledge = list()

    if os.path.isdir(memory_path):
        memories = os.listdir(memory_path)
    else:
        logger.warn("%s missing, i'm useless :(" % memory_path)
        return knowledge

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

def process(action, input) :

    output = list()

    for knowledge in memories() :
        try:
            output.append(getattr(knowledge, action)(input))
        except:
            logger.warn("%s not know how to %s" % (knowledge.__name__, action))

    return output

def ears(words) :

    return process("hear", words)

