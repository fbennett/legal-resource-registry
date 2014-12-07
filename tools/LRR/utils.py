'''
   Utility methods for Legal Resource Registry
'''

import os,sys
from docutils import nodes


class Utils:
    def __init__(self):
        pass

    def makeContainer(self, classname, rawsource=None, text=None, suffix="\n"):
        classnames = classname.split()
        node = nodes.container(rawsource=rawsource, text=text, suffix=suffix)
        for cls in classnames:
            node.attributes["classes"].append(cls)
        return node

    def getRootPath(self):
        pth = os.path.join(os.path.split(sys.argv[0])[0],os.path.pardir)
        pth = os.path.abspath(pth)
        return pth

    def mkGitHubUrl (self,traveler,segment,courtID):
        idlst = courtID.split(";")
        if segment == "reporters":
            reporterID = idlst[-1]
            for i in range(1,len(idlst)-1,1):
                trypth = os.path.join(*[traveler.rootPath,"data",segment] + idlst[0:i] + [reporterID,"index.txt"])
                if os.path.exists(trypth):
                    idlst = idlst[0:i] + [reporterID]
                    break
        return os.path.join(*[traveler.gitHubStub,segment] + idlst + ["index.txt"])

