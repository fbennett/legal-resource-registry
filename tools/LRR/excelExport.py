'''
Write Excel form from jurisdiction data
'''
import re
import xlsxwriter

langLst = [
  "none",
  "Afrikaans (af-ZA)", 
  "Arabic (ar)", 
  "Austrian (de-AT)", 
  "Basque (eu-ES)", 
  "Brazilian Portuguese (pt-BR)", 
  "Bulgarian (bg-BG)", 
  "Catalan (ca-AD)", 
  "Chinese (zh-CN)", 
  "Chinese (zh-TW)", 
  "Croatian (hr-HR)", 
  "Czech (cs-CZ)", 
  "Danish (da-DK)", 
  "Dutch (nl-NL)", 
  "English (en-US)", 
  "Estonian (et-EE)", 
  "Farsi (fa)", 
  "Finnish (fi-FI)", 
  "French (fr-FR)", 
  "Galician (gl-ES)", 
  "German (de)", 
  "Greek (el-GR)", 
  "Hebrew (he-IL)", 
  "Icelandic (is-IS)", 
  "Indonesian (id-ID)", 
  "Italian (it-IT)", 
  "Japanese (ja-JP)", 
  "Khmer (km)", 
  "Korean (ko-KR)", 
  "Laotian (lo)", 
  "Latvian (lv)", 
  "Lithuanian (lt-LT)", 
  "Magyar (hu-HU)", 
  "Mongolian (mn-MN)", 
  "Norwegian Bokmol (nb-NO)", 
  "Norwegian Nynorsk (nn-NO)", 
  "Polish (pl-PL)", 
  "Portuguese (pt-PT)", 
  "Romanian (ro-RO)", 
  "Russian (ru-RU)", 
  "Serbian (sr-RS)", 
  "Slovak (sk-SK)", 
  "Slovene (sl-SI)", 
  "Spanish (es-ES)", 
  "Swedish (sv-SE)", 
  "Swiss German (de-CH)", 
  "Thai (th-TH)", 
  "Turkish (tr-TR)", 
  "Ukranian (uk-UA)", 
  "Uzbek (uz-UZ)", 
  "Vietnamese (vi-VN)"
]

class LRRcol:

    def __init__(self, width):
        self.options = {}
        self.width = width

class LRRWorkbook:

    def __init__(self, filename, countryCode, countryName):
        self.countryCode = countryCode
        self.wb = xlsxwriter.Workbook("%s.xlsx" % filename)
        self.ws = self.wb.add_worksheet()
        self.rowno = 1
        self.cols = {
            "A": LRRcol(1),
            "B": LRRcol(10),
            "C": LRRcol(25),
            "D": LRRcol(20),
            "E": LRRcol(20),
            "F": LRRcol(20),
            "G": LRRcol(20)
            }
        
        self.write_title(countryName, countryCode)
        self.write_instructions()
        self.write_language_list()
        self.write_languages()

    def newline(self):
        self.rowno += 1

    def write_title(self, countryName, countryCode):
        fmt = self.wb.add_format({"bold":True})
        fmt.set_font_size(20)
        fmt.set_align('vcenter')
        self.ws.set_row(self.rowno-1, 40)
        title = "Legal Resource Registry: %s (%s)" % (countryName, countryCode)
        self.ws.merge_range("B%s:G%s" % (self.rowno,self.rowno), title, fmt)
        self.newline()

    def write_instructions(self):
        normal = self.wb.add_format()
        bold = self.wb.add_format({'bold':True})
        fmt = self.wb.add_format({'text_wrap': True})
        fmt.set_align("vcenter")
        fmt.set_border(2)
        fmt.set_border_color('#666666')
        fmt.set_bg_color("#fffe90")
        self.ws.merge_range("B%s:C%s" % (self.rowno,self.rowno), '', fmt)
        self.ws.write_rich_string("B%s" % self.rowno, 'This is an information form for the\nLegal Resource Registry, a project to\nspecify unique referencing identifiers\nfor courts worldwide.\n\nPlease adjust the lists below to\nprovide an accurate picture of the\ncourts in your jurisdiction. Feel\nfree to add categories or change\ntheir names as desired.\n\nUse the ', bold, '[-]', normal, ' and ', bold, '[+]', normal, ' symbols above and\nto the right to hide and reveal fields\nand rows for editing convenience.\n\nSet ', bold, 'Main lang', normal, ' to a primary official\nlanguage of the jurisdiction. If there\nare two official languages, set the\nsecond in ', bold, 'Alt lang', normal, '.\n\nCourt names should be written in the\noriginal, official script. If appropriate,\nenter romanized and translated forms\nin columns ', bold, 'D', normal, ' and ', bold, 'F', normal, '.\n\nSend completed forms to bennett@nagoya-u.jp', fmt)
        self.ws.set_row(self.rowno-1, 380, None, {'level': 1, 'hidden': False})
        self.ws.set_row(self.rowno, None, None, {'collapsed': False})
        self.newline()

    def write_languages(self):
        self.newline()
        if False:
            self.lang_menu_row = self.rowno
        else:
            self.main_lang_rowno = self.rowno
            fmt = self.wb.add_format({"bold":True})
            fmt.set_align('right')
            fmt.set_align('vcenter')
            fmt2 = self.wb.add_format()
            fmt2.set_align('vcenter')
            fmt2.set_underline()
            fmt2.set_bg_color("#cccccc")
            fmt2.set_border(5)
            fmt2.set_border_color("#ffffff")
            self.main_lang = "English (en-US)"
            self.alt_lang = "none"
            self.ws.write("B%s" % self.rowno, "Main lang:", fmt)
            self.ws.data_validation("C%s" % self.rowno, { "validate": "list",
                                            "input_title": "Language:",
                                            "input_message": "choose from the list",
                                            "source": "=$A$%d:$A$%d" % (self.lang_start+1,self.lang_end)
                                            })
            self.ws.write("C%s" % self.rowno, self.main_lang, fmt2)
            self.ws.set_row(self.rowno-1, 20)
        self.newline()
        if not False:
            self.alt_lang_rowno = self.rowno
            self.ws.write("B%s" % self.rowno, "Alt lang:", fmt)
            self.ws.data_validation("C%s" % self.rowno, { "validate": "list",
                                            "input_title": "Language:",
                                            "input_message": "choose from the list",
                                            "source": "=$A$%d:$A$%d" % (self.lang_start,self.lang_end)
                                            })
            self.ws.write("C%s" % self.rowno, self.alt_lang, fmt2)
            self.ws.set_row(self.rowno-1, 25)
        self.newline()

    def write_heading(self, txt):
        self.newline()
        fmt = self.wb.add_format({"bold":True})
        fmt.set_font_size(15)
        fmt.set_bg_color("#cf8e02")
        fmt.set_border()
        self.ws.set_row(self.rowno-1, 20)
        self.ws.merge_range("B%s:F%s" % (self.rowno,self.rowno), txt, fmt)
        self.newline()
        self.write_labels()

    def write_labels(self):
        fmt = self.wb.add_format({"bold":True})
        fmt.set_num_format("@")
        fmt.set_align("vcenter")
        fmt.set_underline()
        fmt.set_bg_color("#cccccc")
        fmt.set_left(2)
        fmt.set_border_color("#ffffff")

        green_fmt = self.wb.add_format({'bg_color': '#C6EFCE',
                                        'font_color': '#006100'})

        red_fmt = self.wb.add_format({'bg_color': '#FFC7CE',
                                        'font_color': '#9C0006'})

        self.ws.data_validation("B%s" % self.rowno, { "validate": "list",
                                        "input_title": "Citeable?",
                                        "input_message": "yes or no",
                                        "source": ["Citable: yes", "Citable: no"]
                                        })
        self.ws.write("B%s" % self.rowno, "Citable: yes")

        self.ws.conditional_format('B%s:B%s' % (self.rowno, self.rowno), {'type':     'text',
                                                                          'criteria': 'containing',
                                                                          'value':     'yes',
                                                                          'format':    green_fmt})

        self.ws.conditional_format('B%s:B%s' % (self.rowno, self.rowno), {'type':     'text',
                                                                          'criteria': 'containing',
                                                                          'value':     'no',
                                                                          'format':    red_fmt})
        self.ws.write("D%s" % self.rowno, "Roman", fmt)
        self.ws.write("E%s" % self.rowno, "English", fmt)
        self.ws.write("G%s" % self.rowno, "URL", fmt)
        self.ws.write_formula("C%s" % self.rowno, "=$C$%s" % self.main_lang_rowno, fmt, 'English (en-US)')
        self.ws.write_formula("F%s" % self.rowno, "=$C$%s" % self.alt_lang_rowno, fmt, 'none')
        self.ws.set_row(self.rowno-1, 20)
        self.newline()

    def write_datarow(self, main, romanized, english, other, url):
        self.write_datacell("C", main)
        self.write_datacell("D", romanized)
        self.write_datacell("E", english)
        self.write_datacell("F", other)
        self.write_datacell("G", url)
        self.ws.set_row(self.rowno - 1, None, None, {'level': 1, 'hidden': False})
        self.newline()

    def write_datacell(self, col, txt):
        if not txt: return
        txt = re.sub("^The\s+", "", txt)
        if int(len(txt)*0.85) > self.cols[col].width:
            self.cols[col].width = int(len(txt)*0.85)
        self.ws.write("%s%s" % (col,self.rowno), txt)

    def set_column_styles(self):
        self.cols["D"].options = {'level':2}
        self.cols["E"].options = {'level':1, 'collapsed':True}
        self.cols["F"].options = {'level':2, 'collapsed':True}
        self.cols["G"].options = {'collapsed':True}

    def set_column_widths(self):
        for col in self.cols.keys():
            self.ws.set_column("%s:%s" % (col,col), self.cols[col].width, None, self.cols[col].options)

    def write_language_list(self):
        self.newline()
        self.lang_start = self.rowno
        for lang in langLst:
            self.ws.write("A%s" % self.rowno,lang)
            self.ws.set_row(self.rowno-1, None, None, {"hidden":1})
            self.newline()
        self.lang_end = (self.rowno-1)

    def close(self):
        self.set_column_styles()
        self.set_column_widths()
        self.wb.close()

