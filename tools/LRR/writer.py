'''
   HMTL rendering translator for Legal Resource Registry
'''

from docutils.writers.html4css1 import HTMLTranslator

class HTMLTranslatorForLegalResourceRegistry(HTMLTranslator):

    def __init__(self, document, **kwargs):
        HTMLTranslator.__init__(self, document, **kwargs)
        settings = self.settings
        #self.d_class = DocumentClass(settings.documentclass)

    def depart_container(self, node):
        ''' Fix suffix handling
        '''
        suffix = "\n"
        if node.attributes.has_key('suffix'):
            suffix = node.attributes['suffix']
        self.body.append('</div>' + suffix)

    def visit_bubble(self, node):
        if node.has_key('title_en'):
            title_en = ' title="%s"' % node["title_en"]
        else:
            title_en = ""
        self.body.append('<a class="reference external" href="%s"%s>%s' % (node['url'],title_en,node['title']))

    def depart_bubble(self, node):
        self.body.append('</a>\n')

    def visit_altwrapper(self, node):
        if node.has_key('title'):
            title = ' title="%s"' % node["title"]
        else:
            title = ""
        self.body.append('<span%s>' % title)

    def depart_altwrapper(self, node):
        self.body.append('</span>\n')

    def visit_court(self, node):
        self.body.append(self.starttag(node, 'h3', CLASS="court").strip())

    def depart_court(self, node): 
        self.body.append('</h3>\n')

    def visit_courtbubble(self, node):
        self.body.append('<a class="bubble" href="%s">' % node["href"])

    def depart_courtbubble(self, node): 
        self.body.append('</a>')

    def visit_minibubble(self, node):
        self.body.append('<a class="bubble mini" href="%s">' % node["href"])

    def depart_minibubble(self, node): 
        self.body.append('</a>')

    def visit_label(self, node):
        self.body.append('<span class="label">')

    def depart_label(self, node): 
        self.body.append('</span>')

    def visit_value(self, node):
        self.body.append('<span class="value">')

    def depart_value(self, node): 
        self.body.append('</span>')

    def visit_valueunconfirmed(self, node):
        self.body.append('<span class="value unconfirmed">')

    def depart_valueunconfirmed(self, node): 
        self.body.append('</span>')

    def visit_valueneutral(self, node):
        self.body.append('<span class="value neutral">')

    def depart_valueneutral(self, node): 
        self.body.append('</span>')

    def visit_featurename(self, node):
        self.body.append('<span class="feature-name">')

    def depart_featurename(self, node): 
        self.body.append('</span>')

    def visit_octiconlink(self, node):
        self.body.append('<span class="octicon octicon-link">')

    def depart_octiconlink(self, node): 
        self.body.append('</span>')

