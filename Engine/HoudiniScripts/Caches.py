import hou
import Engine.engine

def list_all_caches(Engine):
    """list all the cache of a scene"""
    nodes = hou.node("/obj").allSubChildren()
    # print(hou.node("/obj/pyro_import/test"))
    listCache = []
    for n in nodes:
        if n.type().name() == "filecache":
            # print(n.name())
            listCache.append(n)
    return listCache

list_all_caches()
print("goood")