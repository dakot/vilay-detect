# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the testkraut package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Here come the docs....

"""

import logging
lgr = logging.getLogger(__name__)
import argparse
from vilay import config

__docformat__ = 'restructuredtext'

# magic line for manpage summary
# man: -*- % main command

parser_args = dict(formatter_class=argparse.RawDescriptionHelpFormatter)

def setup_parser(parser):
    parser.add_argument('media', help="path of media file", nargs="?")
    
    
def run(args):
    from vilay.vilay_detect import VilayDetect
#     import sys
    
    vd = VilayDetect(False)
    
    if not args.media is None:
        vd.newFile(args.media)
    
    vd.wait()
    
