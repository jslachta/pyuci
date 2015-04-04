pyuci
========

:pyuci: Python UCI module
:Copyright: Copyright (c) 2013 CESNET, z.s.p.o., Jiri Slachta, slachta@cesnet.cz
:License: GPL
:Homepage: http://homeproj.cesnet.cz/projects/besip

What
----

"pyuci" is a python wrapper for Unified Configuration Interface (UCI) - a wrapper
for centralized configuration in OpenWrt.

Requirements
------------

  - Python 2.6 or better (does not include support for Python 3 yet)
  - modules subprocess and os.path are prerequisites for this static library

Usage
-----

To obtain configuration via command uci get for the option callmon.global.host use:

	from pyuci.pyuci import uci
	print uci.get("callmon","global","host")