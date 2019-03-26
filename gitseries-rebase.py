#! /usr/bin/env python3

from common import *
import gitseries

(_, rebase_point, _, _, _) = gitseries.get_editor_params()

try: exout('git rebase --interactive --keep-empty "{}"'.format(rebase_point))
except: pass

