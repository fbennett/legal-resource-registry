'''
   HMTL rendering translator for Legal Resource Registry
'''

from docutils.writers.html4css1 import HTMLTranslator

class HTMLTranslatorForLegalResourceRegistry(HTMLTranslator):

    def __init__(self, document, **kwargs):
        HTMLTranslator.__init__(self, document, **kwargs)
        settings = self.settings
        #self.d_class = DocumentClass(settings.documentclass)

    def visit_floater(self, node):
        if node.has_key('scale'):
            width = ' width="%d"' % int((900 * float(node['scale'])))
        else:
            width = ''
        self.body.append('<div class="floater"><a href="graphics/%s"><img src="graphics/%s"%s></a></div>' % (node['graphic'],node['graphic'],width))

    def depart_floater(self, node):
        pass

    def visit_label(self, node):
        # Context added in footnote_backrefs.
        self.body.append(self.starttag(node, 'td', '%s' % self.context.pop(),
                                       CLASS='label'))

    def depart_label(self, node):
        # Context added in footnote_backrefs.
        self.body.append('%s</td><td>%s' % (self.context.pop(), self.context.pop()))

    def visit_footnote_reference(self, node):
        href = '#' + node['refid']
        format = self.settings.footnote_references
        if format == 'brackets':
            suffix = ''
            self.context.append('')
        else:
            assert format == 'superscript'
            suffix = '<sup>'
            self.context.append('</sup>')
        self.body.append(self.starttag(node, 'a', suffix,
                                       CLASS='footnote-reference', href=href))

    def depart_footnote_reference(self, node):
        self.body.append(self.context.pop() + '</a>')

    def visit_tab(self, node):
        if node.has_key('href'):
            href = ' href="%s"' % node['href']
        else:
            href = ''
        if node.has_key('selected'):
            selected = ' selected'
        else:
            selected = ''
        self.body.append('<div class="tab%s"><a%s>' % (selected, href))

    def depart_tab(self, node):
        self.body.append('</a>\n</div>')

    def visit_breadcrumb(self, node):
        if node.has_key('en'):
            translation = ' title="%s"' % node['en']
        else:
            translation = ''
        self.body.append('<h%s%s>' % (node['level'], translation))

    def depart_breadcrumb(self, node):
        self.body.append('</h%s>' % node['level'])

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
        if node['url'].endswith('.xlsx'):
            cls = ' class="excel"'
        elif node.has_key('class') and node['class'] == 'court':
            cls = ' class="court"'
        else:
            cls = ''
        self.body.append('<a%s href="%s"%s>%s' % (cls,node['url'],title_en,node['title']))

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

    def visit_fieldlabel(self, node):
        self.body.append('<span class="label">')

    def depart_fieldlabel(self, node): 
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

