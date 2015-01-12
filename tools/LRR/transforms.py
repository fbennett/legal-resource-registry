'''
    Transforms for Legal Citation Registry
'''

from docutils import nodes
from docutils.transforms import Transform
from nodes import *

class MoveTrans(Transform):
    default_priority = 100

    def apply(self):

        # self.startnode is the pending marker
        # self.startnode.parent is the translation text
        # self.startnode.parent.parent is the enclosing node, whatever it is

        translation = self.startnode.parent.astext()
        empty = nodes.generated()
        self.startnode.parent.replace_self(empty)

        # Okay, so we want to add a wrapper around children,
        # and make the wrapper the new child of self.startnode.parent.parent

        altie = altwrapper()
        altie["title"] = translation
        for child in self.startnode.parent.parent.children:
            newchild = child.deepcopy()
            altie += newchild
            altie.setup_child(newchild)
        self.startnode.parent.parent.children = [altie]
        self.startnode.parent.parent.setup_child(altie)

