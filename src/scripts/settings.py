#!/usr/bin/env python
from os import path

SCRIPTS_DIR = path.dirname(path.abspath(__file__))
TEMPLATE_DIR = path.normpath(path.join(SCRIPTS_DIR, 'templates'))
PROJECT_DIR = path.normpath(path.join(SCRIPTS_DIR, '..', '..'))
NUMBER_DIR = path.normpath(path.join(PROJECT_DIR, 'src', 'number'))
