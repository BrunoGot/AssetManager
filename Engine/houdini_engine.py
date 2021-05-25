import sys
import os

houdini_path = r"C:\Program Files\Side Effects Software\Houdini 18.5.408" #move it to the configuration file

if hasattr(sys, "setdlopenflags"):
    old_dlopen_flags = sys.getdlopenflags()
    import DLFCN

    sys.setdlopenflags(old_dlopen_flags | DLFCN.RTLD_GLOBAL)
try:
    import hou
except ImportError:
    # Add $HFS/houdini/python2.7libs to sys.path so Python can find the
    # hou module.
    sys.path.append(houdini_path + "\houdini\python2.7libs")
    import hou
finally:
    if hasattr(sys, "setdlopenflags"):
        sys.setdlopenflags(old_dlopen_flags)

"""sys.path.append(
    houdini_path + "\houdini\python2.7libs"
)
import hou"""
print(sys.path)

from engine import Engine

hou.node("./")

class HoudiniEngine(Engine):
    def __init__(self):
        pass