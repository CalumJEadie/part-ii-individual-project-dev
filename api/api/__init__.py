import time
import logging
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def display(text,duration):
    text = text[0:50]

    logger.info("display(text=%s,duration=%s)",text,duration)
    print "text"
    time.sleep(duration)

def ask_yes_no(text):
    """
    :rtype: Boolean
    """

    choice = random.choice([True,False])
    logger.info("ask_yes_no(text=%s) = %s",text,choice)
    return choice