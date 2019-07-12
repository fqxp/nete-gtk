#!/usr/bin/env python

import os
import signal

from dogtail.config import config
from dogtail.procedural import run, focus, click, keyCombo
from dogtail.sessions import Session
from dogtail.tc import TCNode, TCString
from dogtail.utils import screenshot

config.fatalErrors = True
config.runTimeout = 0
config.runInterval = 0

session = Session('/usr/bin/ratpoison')
session.start()

# TestString = TCString()
tcn = TCNode()

pid = run('nete-gtk')
# tcn.compare("app exists", None, focus.application.node)
click.button('New Note')
keyCombo('<Control><Shift>d')
screenshot()


os.kill(pid, signal.SIGTERM)

session.stop()
