from time import strftime
from sqlite3 import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import socket
import bs4
import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime


root = Tk()
root.title(" Student Management System ")
root.geometry("600x600+400+200")    # Creating GUI
root.resizable(width=False, height=False)


def f1():
    root.withdraw()
    adst.deiconify()
    adst_entRno.delete(0, END)
    adst_entName.delete(0, END)
    adst_entMarks.delete(0, END)
    adst_entRno.focus()

# ADD content to the database
def a():
    con = None
    try:
        con = connect("student.db")
        cursor = con.cursor()
        sql = "insert into student values('%d', '%s', %d)"
        rno = int(adst_entRno.get())
        if rno <= 0 or rno == " ":
            showerror("Error", "invalid Roll No")
        else:
            name = adst_entName.get()
            if len(name) < 2:
                showerror("Error", "Invalid Name")
            else:
                marks = int(adst_entMarks.get())
                if marks < 0 or marks > 100:
                    showerror("Error", "Nnvalid Marks")
                else:
                    args = (rno, name, marks)
                    cursor.execute(sql % args)
                    con.commit()
                    showinfo("success", "Record Inserted")
    except Exception as e:
        con.rollback()
        showerror("Error", "Invalid inputs")
    finally:
        if con is not None:
            con.close()


def f2():
    adst.withdraw()
    root.deiconify()


def f3():
    root.withdraw()
    vist.deiconify()

    vist_stData.delete(1.0, END)
    con = None
    try:
        con = connect("student.db")
        cursor = con.cursor()
        sql = "select * from student";
        cursor.execute(sql)
        data = cursor.fetchall()
        info = ""
        for d in data:
            info = info + " rno:" + str(d[0]) + "	name:" + str(d[1]) + "	marks:" + str(d[2]) + "\n"
        vist_stData.insert(INSERT, info)
    except Exception as e:
        showerror("Failure", e)
    finally:
        if con is not None:
            con.close()


def f4():
    vist.withdraw()
    root.deiconify()


def f5():
    root.withdraw()
    upst.deiconify()
    upst_entRno.delete(0, END)
    upst_entName.delete(0, END)
    upst_entMarks.delete(0, END)
    upst_entRno.focus()

# UPDATE content to the database
def u():
    con = None
    try:
        con = connect("student.db")
        cursor = con.cursor()
        sql = "update student set marks= '%r', name='%s' where rno = %r "
        rno = int(upst_entRno.get())
        name = upst_entName.get()
        marks = int(upst_entMarks.get())
        args = (marks, name, rno)
        cursor.execute(sql % args)
        if cursor.rowcount >= 1:
            con.commit()
            showinfo("Success", "Record Updated")
        else:
            showerror("Failure", "Record does not exist")
    except Exception as e:
        con.rollback()
        showerror("failure", e)
    finally:
        if con is not None:
            con.close()


def f6():
    upst.withdraw()
    root.deiconify()


def f7():
    root.withdraw()
    dest.deiconify()

# DELETE content from the database
def d():
    con = None
    try:
        con = connect("student.db")
        cursor = con.cursor()
        sql = "delete from student where rno = '%r'"
        rno = int(dest_entRno.get())
        args = (rno)
        cursor.execute(sql % args)
        if cursor.rowcount >= 1:
            con.commit()
            showinfo("Success", "Record Deleted")
        else:
            showerror("Failure", "Roll no doesnt exist")
    except Exception as e:
        con.rollback()
        showerror("failure", e)
    finally:
        if con is not None:
            con.close()


def f8():
    dest.withdraw()
    root.deiconify()
    dest_entRno.delete(0, END)
    dest_entRno.focus()

# Potting the content of the database
def c():
    con = None
    try:
        ns = []
        mk = []
        con = connect("student.db")
        cursor = con.cursor()
        sql = "select * from student "
        cursor.execute(sql)
        data = cursor.fetchall()
        for d in data:
            ns.append(d[1])
            mk.append(d[2])

        x = np.arange(len(ns))
        plt.bar(x, mk, label='Marks', width=0.75)
        plt.xticks(x, ns)
        plt.xlabel("Names")
        plt.ylabel("Marks")
        plt.legend()
        plt.grid()
        plt.show()

    except Exception as e:
        con.rollback()
        showerror(" Issue ", e)
    finally:
        if con is not None:
            con.close()


btnAdd = Button(root, text="Add", width=10, font=('courier', 18, 'bold'), command=f1)
btnView = Button(root, text="View", width=10, font=('courier', 18, 'bold'), command=f3)
btnUpdate = Button(root, text="Update", width=10, font=('courier', 18, 'bold'), command=f5)
btnDelete = Button(root, text="Delete", width=10, font=('courier', 18, 'bold'), command=f7)
btnCharts = Button(root, text="Chart", width=10, font=('courier', 18, 'bold'), command=c)

lblqoute = Label(root, text="Qoute Of The Day:", font=("calibri", 20, "normal"))
lblqouteans = Label(root, text="", font=("calibri", 15, "bold italic"))
lblqouteans1 = Label(root, text="", font=("calibri", 15, "bold italic"))
lblqouteans2 = Label(root, text="", font=("calibri", 15, "bold italic"))

lblcity = Label(root, text="City:", font=("calibri", 20, "normal"))
lblcityans = Label(root, text="", font=("calibri", 20, "bold"))
lbltemp = Label(root, text="Temperature:", font=("calibri", 20, "normal"))
lbltempans = Label(root, text="", font=("calibri", 20, "bold"))

btnAdd.pack(pady=15)
btnView.pack(pady=15)
btnUpdate.pack(pady=15)
btnDelete.pack(pady=15)
btnCharts.pack(pady=15)
lblqoute.place(x=50, y=470)
lblcity.place(x=50, y=400)
lbltemp.place(x=320, y=400)

adst = Toplevel(root)
adst.title("Add St.")
adst.geometry("500x500+400+100")

adst_lblRno = Label(adst, font=("courier", 18, "bold"), text="enter rno: ")
adst_entRno = Entry(adst, bd=5, font=("courier", 18, "bold"))

adst_lblName = Label(adst, text="enter name: ", font=("courier", 18, "bold"))
adst_entName = Entry(adst, bd=5, font=("courier", 18, "bold"))

adst_lblMarks = Label(adst, text="enter marks: ", font=("courier", 18, "bold"))
adst_entMarks = Entry(adst, bd=5, font=("courier", 18, "bold"))

adst_btnSave = Button(adst, text="Save", font=("courier", 18, "bold"), command=a)
adst_btnBack = Button(adst, text="Back", font=("courier", 18, "bold"), command=f2)

adst_lblRno.pack(pady=10)
adst_entRno.pack(pady=10)
adst_lblName.pack(pady=10)
adst_entName.pack(pady=10)
adst_lblMarks.pack(pady=10)
adst_entMarks.pack(pady=10)
adst_btnSave.pack(pady=10)
adst_btnBack.pack(pady=10)
adst.withdraw()

vist = Toplevel(root)
vist.title("View St. ")
vist.geometry("500x500+400+100")

vist_stData = ScrolledText(vist, width=30, height=10, font=("courier", 18, "bold"))
vist_btnBack = Button(vist, text="Back", font=("courier", 18, "bold"), command=f4)

vist_stData.pack(pady=10)
vist_btnBack.pack(pady=10)
vist.withdraw()

upst = Toplevel(root)
upst.title(" Update St. ")
upst.geometry("500x500+400+100")

upst_lblRno = Label(upst, text="enter rno: ", font=("courier", 18, "bold"))
upst_entRno = Entry(upst, bd=5, font=("courier", 18, "bold"))

upst_lblName = Label(upst, text="enter name: ", font=("courier", 18, "bold"))
upst_entName = Entry(upst, bd=5, font=("courier", 18, "bold"))

upst_lblMarks = Label(upst, text="enter marks: ", font=("courier", 18, "bold"))
upst_entMarks = Entry(upst, bd=5, font=("courier", 18, "bold"))

upst_btnSave = Button(upst, text="Save", font=("courier", 18, "bold"), command=u)
upst_btnBack = Button(upst, text="Back", font=("courier", 18, "bold"), command=f6)

upst_lblRno.pack(pady=10)
upst_entRno.pack(pady=10)
upst_lblName.pack(pady=10)
upst_entName.pack(pady=10)
upst_lblMarks.pack(pady=10)
upst_entMarks.pack(pady=10)
upst_btnSave.pack(pady=10)
upst_btnBack.pack(pady=10)
upst.withdraw()

dest = Toplevel(root)
dest.title(" Delete St. ")
dest.geometry("500x500+400+100")

dest_lblRno = Label(dest, text="enter rno: ", font=("courier", 18, "bold"))
dest_entRno = Entry(dest, bd=5, font=("courier", 18, "bold"))

dest_btnSave = Button(dest, text="Save", font=("courier", 18, "bold"), command=d)
dest_btnBack = Button(dest, text="Back", font=("courier", 18, "bold"), command=f8)

dest_lblRno.pack(pady=10)
dest_entRno.pack(pady=10)
dest_btnSave.pack(pady=10)
dest_btnBack.pack(pady=10)
dest.withdraw()

# For displaying qoute of the day
res = requests.get("https://www.brainyquote.com/quote_of_the_day")
soup = bs4.BeautifulSoup(res.text, "lxml")
data = soup.find("img", {"class": "p-qotd"})
text = data['alt']

# print(len(text))

t1 = text[:52]
t2 = text[51:102]
t3 = text[102:]

lblqouteans.place(x=50, y=505)
lblqouteans['text'] = t1

lblqouteans1.place(x=50, y=535)
lblqouteans1['text'] = t2

lblqouteans2.place(x=50, y=565)
lblqouteans2['text'] = t3

# For city
socket.create_connection(("www.google.com", 80))
res = requests.get("https://ipinfo.io")
data = res.json()
city = data['city']

lblcityans.place(x=110, y=400)
lblcityans['text'] = city

# For temperature
a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
a2 = "&q=" + city
a3 = "&appid=c6e315d09197cec231495138183954bd"
api_address = a1 + a2 + a3
res = requests.get(api_address)
data = res.json()
main = data['main']
temp = main['temp']
temp = (temp * 9/5) + 32
temp = format(temp, ".1f")
temp = str(temp) + "°F"

lbltempans.place(x=450, y=400)
lbltempans['text'] = temp


def time():
    string = strftime('%H:%M:%S')
    lbl.config(text=string)
    lbl.after(1000, time)

lbl = Label(root, font=('calibri', 20, 'bold'), foreground='steelblue')

lbl.pack(pady=10)
lbltime = Label(root, text="Time:", font=("calibri", 20, "normal"))
lbltime.place(x=180, y=330)
time()



date = datetime.datetime.now()

date=date.strftime("%x")
lbl.config(text=date)
lbl.after(1000, time)
lbl = Label(root, font=('calibri', 20, 'bold'),
foreground='steelblue')

lbl.pack(pady=10)
lbldate = Label(root, text="Date:", font=("calibri", 20, "normal"))
lbldate.place(x=180, y=280)

root.mainloop()