# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the vilay package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
""""""

__docformat__ = 'restructuredtext'

__version__ = '0.0.0~pre0'

import os

class _SingletonType(type):
    """Simple singleton implementation adjusted from
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/412551
    """
    def __init__(mcs, *args):
        type.__init__(mcs, *args)
        mcs._instances = {}

    def __call__(mcs, sid, instance, *args):
        if not sid in mcs._instances:
            mcs._instances[sid] = instance
        return mcs._instances[sid]

class __Singleton:
    """To ensure single instance of a class instantiation (object)

    """

    __metaclass__ = _SingletonType
    def __init__(self, *args):
        pass
    # Provided __call__ just to make silly pylint happy
    def __call__(self):
        raise NotImplementedError

