'''
   Utility methods for Legal Resource Registry
'''

import os,sys, re
from docutils import nodes
#from directives import traveler

class reporterPathException(Exception):
    def __init__(self,jurisdiction,reporterKey):
        self.jurisdiction = jurisdiction
        self.reporterKey = reporterKey

class Utils:
    def __init__(self):
        pass

    def splitUrn(self, urn):
        lst = urn.split(";")
        if len(lst) == 1:
            lst = lst[0].split(":")
        elif len(lst) > 1:
            lst = lst[0].split(":") + [lst[1]]
        return lst

    def joinUrn(self, lst, isCourt=False):
        tryLst = ["data/courts"] + lst + ["index.txt"]
        fh = open(os.path.join(*tryLst))
        while 1:
            line = fh.readline()
            if not line: break
            if line.startswith(".. court::"):
                isCourt = True
        if isCourt:
            ret = ":".join(lst[0:-1]) + ";" + lst[-1]
        else:
            ret = ":".join(lst[0:-1])
        return ret

    def courtPathFromJurisdiction(self,rootPath,arg):
        pthlst = [rootPath,"data","courts"]
        pthlst.extend(self.splitUrn(arg))
        pthlst.append("index.txt")
        pth = os.path.join(*pthlst)
        return pth

    def reporterPathFromJurisdiction(self,rootPath,jurisdiction,reporterKey):
        try:
            pthlst = ["data","reporters"]
            pthlst.extend(self.splitUrn(jurisdiction))
        # Drill down
            for i in range(2,len(pthlst),1):
                pth = os.path.join(*pthlst[0:i+1])
                filepth = os.path.join(rootPath,pth,reporterKey,"index.txt")
                if os.path.exists(filepth):
                    return filepth
            raise reporterPathException(jurisdiction,reporterKey)
        except reporterPathException as err:
            print "ERROR: cannot find reporter for %s + %s" % (err.jurisdiction,err.reporterKey)
            sys.exit()

    # Conditions are and-ed if there is more than one
    def checkCondition(self, traveler, newlines):
        for key in traveler.hook.opt.conditional["condition"].keys():
            if not re.match("(?sm).*:%s:.*" % key, newlines):
                return False
        return True

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
        idlst = self.splitUrn(courtID)
        if segment == "reporters":
            reporterID = idlst[-1]
            for i in range(1,len(idlst)-1,1):
                trypth = os.path.join(*[traveler.rootPath,"data",segment] + idlst[0:i] + [reporterID,"index.txt"])
                if os.path.exists(trypth):
                    idlst = idlst[0:i] + [reporterID]
                    break
        return os.path.join(*[traveler.gitHubStub,segment] + idlst + ["index.txt"])

