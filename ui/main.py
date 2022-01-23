"""
MIT License

Copyright (c) 2021-2022 Yilmaz Alpaslan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
try:
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import messagebox
    from tkinter.filedialog import asksaveasfilename
except ModuleNotFoundError or ImportError:
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, "Python 2.x is not supported. Consider using Python 3.x.", "Unsupported Python", 1)
    exit(1)

try:
    from webbrowser import open as openweb
    from perspective import *
    from perspective.errors import *
    import os, sys, subprocess, json
except ModuleNotFoundError or ImportError as details:
    from sys import exc_info
    root = Tk()
    root.withdraw()
    messagebox.showerror("Missing Libraries", str(exc_info()[0]).replace("<class '","").replace("'>","") + ": " + str(exc_info()[1]))
    exit(1)

class Interface(Tk):
    def __init__(self):
        self.height = 503
        self.width = 401
        self.version = "v0.2.0"
        super().__init__()
        self.title("Perpsective API Wrapper")
        self.geometry(f"{self.width}x{self.height}")
        try:
            self.iconbitmap(r"ui\icon.ico")
        except TclError as details:
            if str(details).endswith("not defined"):
                try:
                    self.iconbitmap(r"icon.ico")
                except TclError:
                    pass
        self.minsize(self.width, self.height)
        self.minsize(self.width, self.height)
        self.resizable(height=False, width=False)

        self.initialize_user_interface()
        self.initialize_menu_bar()
        self.initialize_bindings()

    def analyze(self):
        self.analyzeButton.configure(state=DISABLED)
        self.update()
        text = self.varText.get()
        requestedAttributes = []

        if bool(self.varToxicity.get()):requestedAttributes.append("TOXICITY")
        if bool(self.varSevere_Toxicity.get()):requestedAttributes.append("SEVERE_TOXICITY")
        if bool(self.varIdentity_Attack.get()):requestedAttributes.append("IDENTITY_ATTACK")
        if bool(self.varInsult.get()):requestedAttributes.append("INSULT")
        if bool(self.varProfanity.get()):requestedAttributes.append("PROFANITY")
        if bool(self.varThreat.get()):requestedAttributes.append("THREAT")
        if bool(self.varSexually_Explicit.get()):requestedAttributes.append("SEXUALLY_EXPLICIT")
        if bool(self.varFlirtation.get()):requestedAttributes.append("FLIRTATION")
        if bool(self.varAttack_On_Author.get()):requestedAttributes.append("ATTACK_ON_AUTHOR")
        if bool(self.varAttack_On_Commenter.get()):requestedAttributes.append("ATTACK_ON_COMMENTER")
        if bool(self.varIncoherent.get()):requestedAttributes.append("INCOHERENT")
        if bool(self.varInflammatory.get()):requestedAttributes.append("INFLAMMATORY")
        if bool(self.varLikely_To_Reject.get()):requestedAttributes.append("LIKELY_TO_REJECT")
        if bool(self.varObscene.get()):requestedAttributes.append("OBSCENE")
        if bool(self.varSpam.get()):requestedAttributes.append("SPAM")
        if bool(self.varUnsubstantial.get()):requestedAttributes.append("UNSUBSTANTIAL")

        try:
            client = Client(token = "AIzaSyA-yzvgANWE1STU9MTbTLrS3rj1956tVAs", logging_level=None)
        except HTTPException:
            messagebox.showerror("No Internet", "Your internet connection appears to be offline. Please try again later.")
            self.analyzeButton.configure(state=NORMAL)
            return
        try:
            self.response = client.analyze(text=text, attributes=requestedAttributes, language=self.languageSelect.get(), skip_on_lang=bool(self.varSkipOnLang.get()))
        except UnsupportedLanguage as details:
            if self.languageSelect.get() == "Auto detect":
                messagebox.showerror("Unsupported language", f"The language of the text you've entered, {str(details)[:str(details).find(')')].split()[0]}, seems to be unsupported by " + "{} attribute.".format(str(details)[str(details).find("\""):].split()[0].replace("\"", "")))
            else:
                messagebox.showerror("Unsupported language", f"The language you've selected, {str(details)[:str(details).find(')')].split()[0]}, seems to be unsupported by " + "{} attribute.".format(str(details)[str(details).find("\""):].split()[0].replace("\"", "")))
            self.analyzeButton.configure(state=NORMAL)
            return
        self.response = utils.sort_respone(self.response, sort_by="value", order="descending")
        for item in self.resultTreeview.get_children():
            self.resultTreeview.delete(item)
        for attribute, value in self.response.items():
            self.resultTreeview.insert('', END, text=attribute, values=(attribute, value))
        self.analyzeButton.configure(state=NORMAL)
        self.utilMenu.entryconfig(0, state=NORMAL)
        self.utilMenu.entryconfig(1, state=NORMAL)
        self.utilMenu.entryconfig(3, state=NORMAL)
        self.exportJSONButton.configure(state=NORMAL)
        self.copyJSONButton.configure(state=NORMAL)

    def save_graph(self, event = None):
        path = asksaveasfilename(title="Save bar chart as image", filetypes=(("Portable Network Graphics", "*.png"), ), initialfile="chart.png")
        if not not path:
            utils.save_graph(response=self.response, filename=path, grid_lines=True)
            messagebox.showinfo("Successfull", "The bar chart has been successfully saved to the specified path.")

    def save_data(self, event = None):
        path = asksaveasfilename(title="Save the response as a database file", filetypes=(("SQLite3 Database", "*.sqlite3"), ("Typical Database", "*.db"), ), initialfile="response.sqlite3")
        if not not path:
            utils.save_data(response=self.response, filename=path, sort_by="descending")
            messagebox.showinfo("Successfull", "The response has been successfully saved to a database file in the specified directory.")

    def export_json(self, event = None):
        path = asksaveasfilename(title="Save the response as a JSON file", filetypes=(("JSON File", "*.json"), ("All Files", "*.*"), ), initialfile="response.json")
        if not not path:
            utils.export_json(response=self.response, filename=path)
            messagebox.showinfo("Successfull", "The response has been successfully exported in JSON format.")

    def initialize_user_interface(self):
        self.textFrame = LabelFrame(self, text="Text", height=78, width=381)
        self.textFrame.place(x=10, y=2)

        def varTextCallback(*args, **kwargs):
            if self.varText.get() != "":
                self.clearButton.configure(state=NORMAL)
                newAllCheckButtons = []
                for variable in self.allCheckButtons:
                    newAllCheckButtons.append(variable.get())
                if 1 in newAllCheckButtons:
                    self.analyzeButton.configure(state=NORMAL)
                else:
                    self.analyzeButton.configure(state=DISABLED)
            else:
                self.clearButton.configure(state=DISABLED)
                self.analyzeButton.configure(state=DISABLED)

        def checkButtonCallback(*args, **kwargs):
            newAllCheckButtons = []
            for variable in self.allCheckButtons:
                newAllCheckButtons.append(variable.get())
            if 1 in newAllCheckButtons:
                if self.varText.get() != "":
                    self.analyzeButton.configure(state=NORMAL)
                else:
                    self.analyzeButton.configure(state=DISABLED)
            else:
                self.analyzeButton.configure(state=DISABLED)

        self.varText = StringVar()
        self.varText.trace("w", varTextCallback)
        self.textEntry = Entry(self.textFrame, width=59, takefocus=0, textvariable=self.varText)
        self.textEntry.place(x=7, y=0)

        self.pasteButton = Button(self.textFrame, width=15, text="Paste", state=NORMAL, command=lambda: self.textEntry.insert(0, self.clipboard_get()), takefocus=0)
        self.clearButton = Button(self.textFrame, width=15, text="Clear", state=DISABLED, command=lambda: self.textEntry.delete(0, END), takefocus=0)
        self.pasteButton.place(x=6, y=27)
        self.clearButton.place(x=113, y=27)

        self.attrsFrame = LabelFrame(self, text="Requested Attributes", height=195, width=381)
        self.attrsFrame.place(x=10, y=85)

        self.varToxicity = IntVar();self.varToxicity.set(1);self.radioToxicity = Checkbutton(self.attrsFrame, text="Toxicity", takefocus=0, variable=self.varToxicity, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varSevere_Toxicity = IntVar();self.varSevere_Toxicity.set(0);self.radioSevere_Toxicity = Checkbutton(self.attrsFrame, text="Severe Toxicity", takefocus=0, variable=self.varSevere_Toxicity, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varIdentity_Attack = IntVar();self.varIdentity_Attack.set(0);self.radioIdentity_Attack = Checkbutton(self.attrsFrame, text="Identity Attack", takefocus=0, variable=self.varIdentity_Attack, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varInsult = IntVar();self.varInsult.set(0);self.radioInsult = Checkbutton(self.attrsFrame, text="Insult", takefocus=0, variable=self.varInsult, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varProfanity = IntVar();self.varProfanity.set(0);self.radioProfanity = Checkbutton(self.attrsFrame, text="Profanity", takefocus=0, variable=self.varProfanity, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varThreat = IntVar();self.varThreat.set(0);self.radioThreat = Checkbutton(self.attrsFrame, text="Threat", takefocus=0, variable=self.varThreat, onvalue=1, offvalue=0, command=checkButtonCallback)

        self.varFlirtation = IntVar();self.varFlirtation.set(0);self.radioFlirtation = Checkbutton(self.attrsFrame, text="Flirtation", takefocus=0, variable=self.varFlirtation, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varSexually_Explicit = IntVar();self.varSexually_Explicit.set(0);self.radioSexuallyExplicit = Checkbutton(self.attrsFrame, text="Sexually Explicit", takefocus=0, variable=self.varSexually_Explicit, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varAttack_On_Author = IntVar();self.varAttack_On_Author.set(0);self.radioAttackAuthor = Checkbutton(self.attrsFrame, text="Attack on Author", takefocus=0, variable=self.varAttack_On_Author, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varAttack_On_Commenter = IntVar();self.varAttack_On_Commenter.set(0);self.radioAttackCommenter = Checkbutton(self.attrsFrame, text="Attack on Commenter", takefocus=0, variable=self.varAttack_On_Commenter, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varIncoherent = IntVar();self.varIncoherent.set(0);self.radioIncoherent = Checkbutton(self.attrsFrame, text="Incoherent", takefocus=0, variable=self.varIncoherent, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varInflammatory = IntVar();self.varInflammatory.set(0);self.radioInflammatory = Checkbutton(self.attrsFrame, text="Inflammatory", takefocus=0, variable=self.varInflammatory, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varLikely_To_Reject = IntVar();self.varLikely_To_Reject.set(0);self.radioLikely_To_Reject = Checkbutton(self.attrsFrame, text="Likely to Reject", takefocus=0, variable=self.varLikely_To_Reject, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varObscene = IntVar();self.varObscene.set(0);self.radioObscene = Checkbutton(self.attrsFrame, text="Obscene", takefocus=0, variable=self.varObscene, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varSpam = IntVar();self.varSpam.set(0);self.radioSpam = Checkbutton(self.attrsFrame, text="Spam", takefocus=0, variable=self.varSpam, onvalue=1, offvalue=0, command=checkButtonCallback)
        self.varUnsubstantial = IntVar();self.varUnsubstantial.set(0);self.radioUnsubstantial = Checkbutton(self.attrsFrame, text="Unsubstantial", takefocus=0, variable=self.varUnsubstantial, onvalue=1, offvalue=0, command=checkButtonCallback)

        self.allCheckButtons = [self.varToxicity, self.varSevere_Toxicity, self.varIdentity_Attack,
            self.varInsult, self.varProfanity, self.varThreat, self.varFlirtation, self.varSexually_Explicit,
            self.varAttack_On_Author, self.varAttack_On_Commenter, self.varIncoherent, self.varInflammatory,
            self.varLikely_To_Reject, self.varObscene, self.varSpam, self.varUnsubstantial]

        self.radioToxicity.place(x=5, y=0)
        self.radioSevere_Toxicity.place(x=180, y=0)
        self.radioIdentity_Attack.place(x=5, y=20)
        self.radioInsult.place(x=180, y=20)
        self.radioProfanity.place(x=5, y=40)
        self.radioThreat.place(x=180, y=40)

        self.radioFlirtation.place(x=5, y=70)
        self.radioSexuallyExplicit.place(x=180, y=70)
        self.radioAttackAuthor.place(x=5, y=90)
        self.radioAttackCommenter.place(x=180, y=90)
        self.radioIncoherent.place(x=5, y=110)
        self.radioInflammatory.place(x=180, y=110)
        self.radioLikely_To_Reject.place(x=5, y=130)
        self.radioObscene.place(x=180, y=130)
        self.radioSpam.place(x=5, y=150)
        self.radioUnsubstantial.place(x=180, y=150)

        self.languageLabel = Label(self, text="Language:", takefocus=0)
        self.languageLabel.place(x=7, y=285)

        languages = ["Auto detect", "Arabic (ar)", "Chinese (zh)", "Czech (cs)", "Dutch (nl)", "English (en)", "French (fr)",
        "German (de)", "Hindi (hi)", "Hinglish (hi-Latn)", "Indonesian (id)", "Italian (it)", "Japanese (ja)",
        "Korean (ko)", "Polish (pl)", "Portuguese (pt)", "Russian (ru)", "Spanish (es)"]
        self.varLanguage = StringVar()
        self.languageSelect = Combobox(self, width=17, textvariable=self.varLanguage, values=languages, state="readonly", text="Select a language", takefocus=0)
        self.languageSelect.place(x=70, y=285)
        self.languageSelect.set("Auto detect")

        self.varSkipOnLang = IntVar()
        self.varSkipOnLang.set(0)
        self.skipOnLang = Checkbutton(self, text="Skip on unsupported language", takefocus=0, onvalue=1, offvalue=0, variable=self.varSkipOnLang)
        self.skipOnLang.place(x=205, y=285)

        treeviewColumns = ("attr", "scoreval")
        self.resultTreeview = Treeview(self, columns=treeviewColumns, show="headings", height=5, takefocus=0)
        self.resultTreeview.heading('attr', text='Atribute')
        self.resultTreeview.column("attr", minwidth=0, width=247, stretch=False)
        self.resultTreeview.heading('scoreval', text='Score Value')
        self.resultTreeview.column("scoreval", minwidth=0, width=115, stretch=False)
        
        self.treeviewScroll = Scrollbar(self, orient=VERTICAL, command=self.resultTreeview.yview)
        self.resultTreeview.configure(yscroll=self.treeviewScroll.set)
        self.treeviewScroll.place(x=375, y=314, height=127)
        self.resultTreeview.place(x=10, y=314)

        self.analyzeButton = Button(self, text="Analyze", width=24, takefocus=0, state=DISABLED, command=lambda: self.analyze())
        self.analyzeButton.place(x=9, y=449)

        self.exportJSONButton = Button(self, text="Export JSON", width=16, takefocus=0, command=self.export_json, state=DISABLED)
        self.exportJSONButton.place(x=172, y=449)

        self.copyJSONButton = Button(self, text="Copy JSON", width=16, takefocus=0, command=lambda: (self.clipboard_clear(), self.clipboard_append(str(json.dumps(self.response, indent=4)))), state=DISABLED)
        self.copyJSONButton.place(x=286, y=449)

    def initialize_menu_bar(self):
        self.menuBar = Menu(self)

        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label = "View source", accelerator="Alt+S", command=lambda: subprocess.Popen([sys.executable.replace("python.exe", "pythonw.exe"), sys.exec_prefix + "\\Lib\\idlelib\\idle.pyw", os.path.realpath(__file__)]))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "GitHub page", command=lambda: openweb("https://github.com/Yilmaz4/perspective.py"))
        self.fileMenu.add_command(label = "PyPI page", command=lambda: openweb("https://pypi.org/project/perspective.py"))
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Close", accelerator="Alt+F4", command=lambda: self.destroy())
        self.menuBar.add_cascade(label = "File", menu=self.fileMenu)

        self.utilMenu = Menu(self.menuBar, tearoff=0)
        self.utilMenu.add_command(label = "Show graph", command=lambda: utils.show_graph(self.response), state=DISABLED, accelerator="Alt+G")
        self.utilMenu.add_command(label = "Save graph", command=self.save_graph, state=DISABLED, accelerator="Ctrl+G")
        self.utilMenu.add_separator()
        self.utilMenu.add_command(label = "Save data", command=self.save_data, state=DISABLED, accelerator="Ctrl+D")
        self.menuBar.add_cascade(label = "Utilities", menu=self.utilMenu)

        self.config(menu=self.menuBar)
    
    def initialize_bindings(self):
        def show_graph(event = None):
            utils.show_graph(self.response)
        def view_source(event = None):
            subprocess.Popen(f"\"{sys.executable}\" -m idlelib \"{os.path.realpath(__file__)}\"")
        def analyze(event = None):
            newAllCheckButtons = []
            for variable in self.allCheckButtons:
                newAllCheckButtons.append(variable.get())
            if 1 in newAllCheckButtons and self.varText.get() != "":
                self.analyze()
        def give_focus(event = None):
            self.after(50, lambda: self.textEntry.focus())

        self.bind("<Control_L>d", self.save_data)
        self.bind("<Control_L>g", self.save_graph)
        self.bind("<Alt_L>g", show_graph)
        self.bind("<Alt_L>s", view_source)
        self.bind("<Return>", analyze)
        self.bind("<Tab>", give_focus)

if __name__ == "__main__":
    root = Interface()
    root.mainloop()