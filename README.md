# Whow

## About

**Whow** - When, How?

Whow is a CLI To-do application, with features such as:
 * A calendar that supports features like tags and importance,
 * To-Dos (of course)
 * Events

And counting. Whow is a CLI application rewritten in Python with more features than the old shell-script version that can be found [here.](https://github.com/DaringCuteSeal/whow) It aims to include extra features such as

 * Filesystem Structure for organizing files
 * A `toml` configuration instead of a simple `rc`

and more to come.

## Installation
Figure it out yourself. We are exhausted, proper docs will come in a later version, just you wait.

## Currently Working on:

 * Python 3.9 support (for PyPy's sake)
 * Code refactoring
 * Use TOML dates instead of string dates

## Planned Features (high priority):
 * [x] Use TOML dates instead of string dates
 * [x] add support for PyPy3.9 (maybe)
 * [ ] Refactor code for the whow API
 * [ ] Schedule Feature
 * [ ] get this on the PyPI
 * [ ] OTA Update tool
 * [ ] Daily Schedule
 * [ ] Sorting To-Dos and events by time
 * [ ] Document our code also for the whow API

## Planned features (low priority):
 * [ ] Reminders
 * [ ] `whowd`, a daemon for whow using things like libnotify
 * [ ] A reference implementation for an alternative frontend
 * [ ] `curses` frontend to whow
