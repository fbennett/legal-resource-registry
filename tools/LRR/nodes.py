'''
   Nodes used by Legal Resource Registry
'''
from docutils import nodes

class court (nodes.TextElement): pass
class courtbubble (nodes.Inline, nodes.TextElement): pass
class minibubble (nodes.TextElement): pass
class bubble (nodes.Inline, nodes.TextElement): pass
class fieldlabel (nodes.Inline, nodes.TextElement): pass
class value (nodes.Inline, nodes.TextElement): pass
class valueunconfirmed (nodes.Inline, nodes.TextElement): pass
class valueneutral (nodes.Inline, nodes.TextElement): pass
class featurename (nodes.Inline, nodes.TextElement): pass
class octiconlink (nodes.Inline, nodes.TextElement): pass
class altwrapper (nodes.Inline, nodes.TextElement): pass
class trans (nodes.Inline, nodes.TextElement): pass
class breadcrumb (nodes.TextElement): pass
class tab(nodes.TextElement): pass

from manual import floater
