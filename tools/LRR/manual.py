'''
    Handy extensions for documentation
'''

from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.writers.latex2e import LaTeXTranslator

class floater (nodes.TextElement): pass

FloaterTemplate = '''
\\setlength{\\scratchlengthouter}{%s\\textwidth}
\\setlength{\\scratchlengthinner}{\\scratchlengthouter}
\\addtolength{\\scratchlengthinner}{-5pt}
\\begin{floatingfigure}[r]{\\scratchlengthouter}
\\noindent\\begin{minipage}{\\scratchlengthouter}\\hspace{5pt}\\includegraphics[width=\\scratchlengthinner]{%s}
\\end{minipage}
\\end{floatingfigure}

'''

class FloaterDirective(Directive):
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    has_content = False
    option_spec = {
      'scale': directives.unchanged
    }
    def run (self):
        newnode = floater(rawsource=self.arguments[0])
        newnode['graphic'] = self.arguments[0]
        newnode['scale'] = self.options['scale']
        return [newnode]

class LaTeXTranslatorForProjects(LaTeXTranslator):

    def __init__(self, document, **kwargs):
        LaTeXTranslator.__init__(self, document, **kwargs)
        settings = self.settings
        #self.d_class = MLZDocumentClass(settings.documentclass,
        #                             settings.use_part_section)
        #self.d_class = MLZDocumentClass(settings.documentclass)

    def visit_floater(self, node):
        self.out.append(FloaterTemplate % (node['scale'], node['graphic']))

    def depart_floater(self, node):
        pass
