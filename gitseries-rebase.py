#! /usr/bin/env python3

from common import *
import gitseries

cs = gitseries.CurrentSeries()

try: exout('git rebase --interactive --keep-empty "{}"'.format(cs.rebase_point))
except: pass

