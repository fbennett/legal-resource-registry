from LRR import Hook as HookBase

class MyAmazingDataClass:
    def __init__(self):
        self.my_truth = False
        self.courts_in_english = []

class Hook(HookBase):
    def __init__(self):
        HookBase.__init__(self, Data=MyAmazingDataClass)
        self.opt.jurisdiction = "jp"            

    def court(self, options, arg):
        if options.has_key('en'):
            self.data.courts_in_english.append(options['en'])
        else:
            self.data.courts_in_english.append(arg)

    def reporter_start(self, options, dates, arg):
        pass

    def reporter_end(self, options, arg):
        pass

    def variation(self, arg):
        pass

    def export(self):
        self.data.courts_in_english.sort()
        for court in self.data.courts_in_english:
            print court

