# @author divesli
# @date 2014/10/24 18:35:09
#

import sublime, sublime_plugin
import datetime,time
import os,getpass

class PhpHeaderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = edit
        self.tab = self.creat_tab(self.view)
        self.tab.window().show_input_panel("New file name:", "", self.do_input, None, self.do_cancel)
        self.setSyntax()
        self.tab.set_encoding("UTF-8")
        
        #self.tab.set_line_endings("linux")

    def do_input(self, txt):
        try:
            if len(txt.strip()) == 0:
                txt = "Demo"

            self.tab.set_name(txt+".php")
        finally:
            self.setTag()
    
    def do_cancel(self):
        self.setTag()

    def creat_tab(self, view):
        win = view.window()
        tab = win.new_file()
        return tab

    def setTag(self):
        c = self.getCopyRight()
        i = self.getDesc()
        d = self.getDemo()
        h = c + "\n\n" + i + "\n\n" + d
        self.tab.insert(self.edit, 0, h)
        self.setCursor(self.tab, self.edit)

    def setSyntax(self):
        self.tab.set_syntax_file("Packages/PHP/PHP.tmLanguage")
        self.tab.settings().set('default_extension', "php")

    def showMessage(self,txt):
        sublime.message_dialog(txt)

    def setCursor(self, view, edit): 
        key = "@brief:"
        region = sublime.Region(0,view.size())
        point = view.substr(region).find(key) 
        row,col = view.rowcol(point)    
        pt = view.text_point(row,col+len(key)+1)

        view.sel().clear()
        view.sel().add(sublime.Region(pt))

        view.show(pt)
        #pass
           

    def getDemo(self):
        fname = self.getFileName()
        s = "."
        try:
            p = fname.index(s)
            clname = fname[:p]
        except:
            clname = fname

        if len(clname.strip()) == 0:
            clname = "Demo"

        demo =  "class " + clname + " {\n\n"
        demo += "    /**\n"
        demo += "     *\n"
        demo += "     * @brief: construct functon\n"
        demo += "     */\n"
        demo += "    public function __construct() {\n"
        demo += "        //TODO \n"
        demo += "    }\n"
        demo += "}\n"
        return demo


    def getCopyRight(self):
        tmpl = "<?php\n"
        tmpl += "/"
        tmpl += "*" * 79
        tmpl += "\n"
        tmpl += " *\n"
        tmpl += " * Copyright (c) "
        tmpl += self.getYear() + " " + self.getDomain() +", Inc. All Rights Reserved\n"
        tmpl += " * $Id$\n"
        tmpl += " *\n"
        tmpl += " "
        tmpl += "*" * 79
        tmpl += "/"
        return tmpl

    def getDesc(self):
        desc = "/**\n"
        desc += " * @file " + self.getFileName() + "\n"
        desc += " * @author " + self.getUser() + "(" + self.getMail() + ")" + "\n"
        desc += " * @date " + self.getTime() + "\n"
        desc += " * @version " + self.getVersion() + "\n"
        desc += " * @filecoding " + self.getFileCode() + "\n"
        desc += " * @brief: \n"
        desc += " *\n"
        desc += " */"
        return desc

    def getDate(self, format = '%Y/%m/%d %H:%M:%I'):
        t = time.time()
        d = datetime.datetime.fromtimestamp(t)
        return d.strftime(format)

    def getYear(self):
        y = self.getDate('%Y')
        return y

    def getFileName(self):
        #return os.path.basename(self.view.file_name())
        return self.tab.name()

    def getUser(self):
        return getpass.getuser()

    def getMail(self):
        return self.getUser() + "@" + self.getDomain()

    def getTime(self):
        tm = self.getDate()
        return tm

    def getVersion(self):
        return "$Revision 1.0$"

    def getFileCode(self):
        return "UTF-8"

    def getDomain(self):
        return "xxx.cn"


class PhpDocsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        point = self.view.sel()[0].a
        rowrgn = self.view.line(point)
        row,col = self.view.rowcol(point)
        region = sublime.Region(point, rowrgn.begin())
        string = self.view.substr(region).strip()
        docs = ''
        if string == "/**":
            docs = self.getDocs(self.view,point)
        else:
            self.view.run_command("insert",{"characters": "\n"})
            return 
            
        pt = rowrgn.end()
        self.view.insert(edit, pt, docs)

        pxy = self.view.text_point(row+2,col+len("@brief: "))

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pxy))

        self.view.show(pxy)

    def getDocs(self,view,point):
        row,col = view.rowcol(point)
        pxy = view.text_point(row+1,0)
        string = view.substr(view.full_line(pxy)).strip()
        x = string.find("(")
        y = string.find(")")  
        strParams = string[x+1:y] 
        params = strParams.split(",") 
        space = " " * (col -2)
        docs = "\n"
        docs += space + "*\n"
        docs += space + "* @brief: \n"
        for param in params:
            docs += space + "* @param " + param.strip() + ": \n"
        docs += space + "* @return: \n"
        docs += space + "*/"
        return docs
