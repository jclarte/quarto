"""
main entry point for the quarto game
"""
import argparse
import logging

LOG = logging.getLogger(__file__)

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument('--debug', '-d', action='store_true')

args = argument_parser.parse_args()

if args.debug:
    logging.basicConfig(level='DEBUG')
    LOG.info("debug mode activated")

print("Hello Quarto !")

from src import GameRunner

GameRunner().run()