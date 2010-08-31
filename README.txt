Introduction
============

Local Development
=================
Create local buildout config:-

$ cat - >> local.cfg
[buildout]
extends = buildout.cfg

[django]
settings = dev_settings
^D

Create local settings:-

$ cat - > kecupu/pos/dev_settings.py
from kecupu.pos.settings import *

DATABASE_NAME = 'kecupu_dev.db'
^D
