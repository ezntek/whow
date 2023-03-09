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

## WHAT IS HAPPENING RIGHT NOW?!
Because the old codebase was

1. a prototype
2. extremely messy and inconsistent

I (ezntek) am re-working the ENTIRE CODEBASE, so do NOT expect working code at all. The CLI will now be seperated from the main API. If you are coming from the blog pots, you have been warned!!

## What's going to change in the new codebase?

1. `tomli` and `tomli_w`
2. Drop PyPy support, because typing on 3.9 is not nice.
3. Isolate the code into an API, and the CLI will serve as a reference implementation of the API with a user interface.
4. Better structuring and python packages.
5. The backend of everything, such as the toml storage format for todos, schedules, events, etc.

## Planned Features (high priority):
 * [x] Use TOML dates instead of string dates
 * [x] Refactor code for the whow API
 * [x] Schedule Feature
 * [ ] Calendar date highlighting
 * [ ] get this on the PyPI
 * [ ] OTA Updates
 * [ ] Sorting To-Dos and events by time
 * [ ] Document our code also for the whow API

## Planned features (low priority):
 * [ ] Reminders
 * [ ] `whowd`, a daemon for whow using things like libnotify
 * [ ] A reference implementation for an alternative frontend
 * [ ] `curses` frontend to whow