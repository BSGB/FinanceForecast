import tkinter
from tkinter import ttk

from KNN import KNN
from LinearReg import LinearReg
from PolyInter import PolyInter
import gc

class Interfejs(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):

        self.grid()

        self.labelVar1 = tkinter.StringVar()
        self.labelVar1.set(u"Wybierz algorytm: ")
        label1 = tkinter.Label(self, textvariable=self.labelVar1, anchor="w", fg="black", bg='white')
        label1.grid(column=0,row=0,sticky='EW')

        self.alghoritm = tkinter.StringVar()
        self.cbAlghoritm = ttk.Combobox(self, textvariable=self.alghoritm)
        self.cbAlghoritm.bind("<<ComboboxSelected>>", self.getAlghoritm)
        self.cbAlghoritm.grid(column=1, row=0)
        self.cbAlghoritm['values'] = ('LinearReggresion', 'KNN', 'PolyInter')

        self.labelVar2 = tkinter.StringVar()
        self.labelVar2.set(u"Wybierz spółkę: ")
        label2 = tkinter.Label(self, textvariable=self.labelVar2, anchor="w", fg="black", bg="white")
        label2.grid(column=0,row=1,sticky='EW')

        self.company = tkinter.StringVar()
        self.cbCompany = ttk.Combobox(self, textvariable=self.company)
        self.cbCompany.bind("<<ComboboxSelected>>", self.getCompany)
        self.cbCompany.grid(column=1,row=1)
        self.cbCompany['values'] = ('INTC', 'AAPL')

        self.labelVar3 = tkinter.StringVar()
        self.labelVar3.set(u"Wybierz split: ")
        label3 = tkinter.Label(self, textvariable=self.labelVar3, anchor="w", fg="black", bg="white")
        label3.grid(column=0,row=2,sticky='EW')

        self.split = tkinter.StringVar()
        self.cbSplit = ttk.Combobox(self, textvariable=self.split)
        self.cbSplit.bind("<<ComboboxSelected>>", self.getSplit)
        self.cbSplit.grid(column=1,row=2)
        self.cbSplit['values'] = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)

        self.buttonVar = tkinter.StringVar()
        self.buttonVar.set(u"START")
        button = ttk.Button(self, textvariable=self.buttonVar, command=self.onButtonClick)
        button.grid(column=3, row=5)


        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)


    def getAlghoritm(self, event):
        global alg
        alg = self.cbAlghoritm.get()
        return alg

    def getCompany(self, event):
        global cmp
        cmp = self.cbCompany.get()
        return cmp

    def getSplit(self, event):
        global split
        split = self.cbSplit.get()
        return split

    def onButtonClick(self):
        x = 0
        if(alg == 'KNN'):
            x = KNN(cmp, float(split))
            x.main()
        elif(alg == 'LinearReggresion'):
            x = LinearReg(cmp, float(split))
            x.plots()
        elif(alg == 'PolyInter'):
            x = PolyInter(cmp, float(split))
            x.plots()


if __name__ == "__main__":
    app = Interfejs(None)
    app.title('Interfejs')
    app.mainloop()



