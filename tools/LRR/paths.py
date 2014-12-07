'''
   Paths utility for Legal Resource Registry
'''

import os

class PathTool:
    
    def __init__(self):
        pass

    def courtPathFromJurisdiction(self,arg):
        pthlst = ["data","courts"]
        pthlst.extend(arg.split(";"))
        pthlst.append("index.txt")
        pth = os.path.join(*pthlst)
        return pth

    def reporterPathFromJurisdiction(self,jurisdiction,reporterKey):
        pthlst = ["data","reporters"]
        pthlst.extend(jurisdiction.split(";"))
        # Drill down
        for i in range(2,len(pthlst),1):
            pth = os.path.join(*pthlst[0:i+1])
            filepth = os.path.join(pth,reporterKey,"index.txt")
            if os.path.exists(filepth):
                return filepth
        raise reporterPathException(jurisdiction,reporterKey)

