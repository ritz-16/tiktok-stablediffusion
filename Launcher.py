#Python3 code goes here
import mysql.connector
import itertools, shutil, os
from python1 import tiktokapi#Driver function from python1 module
from dream import dreamer#Driver function from dream module
import os.path
import time
import threading
from tkinter import *
from PIL import ImageTk,Image
mydb=mysql.connector.connect(host='localhost',user='root',password='@Padartha1',database='tiktoksd')#Connecting to the mysql database

maincounter=1#counter to keep track of the images we are reading from db

root=Tk()
root.title("Comments to image generator")
root.geometry('550x550')
myfont2=('Times',22,'bold')
label4=Label(root,text='Comment and create your own art !',font=myfont2,fg='orange',relief='flat')
label4.grid(row=1,column=4)
myfont1=('Times',14)
label0=Label(root,text='UserName',font=myfont1,width=15,fg='orange',bg='white',borderwidth=2,relief='raised')#username
label0.grid(row=4,column=2)
#The label which shows the username
label1=Label(root,text='UserName')#username
label1.grid(row=5,column=2)
#inputField=Entry(root,width=40)
#inputField.grid(row=2,column=4)
#def myclick():
    #unique_id=inputField.get()
label3=Label(root,text='Comments',font=myfont1,width=15,fg='orange',bg='white',borderwidth=2,relief='raised')#comments
label3.grid(row=4,column=4)
#The label which shows the comments
label2=Label(root,text='Comments')#comments
label2.grid(row=5,column=4)
canvas=Canvas(root,height=300,width=300)
canvas.grid(row=12,column=4,pady=25,padx=25)
cur_path='/Users/ritamghosh/Desktop/stable-diffusion/outputs/img-samples/welcome.png'
pil_img = Image.open(cur_path).resize((300, 300))
img=ImageTk.PhotoImage(pil_img)
imageContainer=canvas.create_image(0,0,anchor='nw',image=img)
canvas.itemconfigure(imageContainer, image=img)
startButton=Button(root,text='Stop!!',command=root.quit)
startButton.grid(row=3,column=4,pady=40,padx=35)

#canvas.mainloop()

def refresh_image(canvas, img, image_path, image_id):
    try:
        #print(cur_path, os.path.exists(cur_path))
        pil_img = Image.open(cur_path).resize((300, 300))
        img = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(image_id, image=img)
    except:
        pass
    # repeat every half sec
    canvas.after(20, refresh_image, canvas, img, image_path, image_id)

def AutoRefresh():
    RefreshText()
    # threading.Thread(target=playsound('tone.mp3'))
    root.after(1000, func=AutoRefresh)

def RefreshText():
    global cur_path,maincounter
    print(str(maincounter)+'start of loop')
    cursor1 = mydb.cursor()
    cursor1.execute("select count(*) from data1")
    c = cursor1.fetchone()

    # cursor1.execute("update Tiktok_Live_Data set filestatus = 0 where id=" + str(count - 1))
    # cursor1.execute("update Tiktok_Live_Data set filestatus = 1 where id=" + str(count))
    cursor1.execute("select * from data1 where id=" + str(maincounter))
    maincounter += 1
    datas = cursor1.fetchone()
    cur_path = datas[3]

    

    try:
        label1.config(text=datas[1])
    except:
        label1.config(text="@User")  # Default
    try:
        label2.config(text=datas[2])
    except:
        label2.config(text="Great!!")  # Default

    def SDdriver():
        dreamer(maincounter-1)
    path = datas[3]
    #print(path)
    if not os.path.exists(path):
        print(str(maincounter)+'before sd')
        SDdriver()
        print(str(maincounter)+'after sd')
        #time.sleep(5)








def Loop():
    global maincounter
    global imageContainer
    global cur_path
    cursor1=mydb.cursor()
    sql1=('use tiktoksd')
    cursor1.execute(sql1)
    sql2=('select * from data where id=%s')
    data2=(maincounter,)
    cursor1.execute(sql2,data2)
    results=cursor1.fetchone()
    if(os.path.exists(results[3])):
        '''pil_img = Image.open(cur_path).resize((500, 400))
        img = ImageTk.PhotoImage(pil_img)
        canvas.itemconfigure(image_id, image=img)'''
        #imagine.configure(image=myimg)#change the label
        #imagine.grid(row=6,column=6,pady=25,padx=25)
        #image.after(200,Loop)#recursion to keep changing.
        maincounter+=1#incrementing the global counter
        label1.configure(text=results[1])
        #label1.after(200,Loop)
        label2.configure(text=results[2])
        #label3.configure(image=results[3])
        #label3.after(600,Loop)
        #imagine.after(600,Loop)
        cur_path=results[3]
        pil_img = Image.open(cur_path).resize((500, 400))
        myimg=ImageTk.PhotoImage(pil_img)#change the image path
        canvas.itemconfigure(imageContainer,image=myimg)
        canvas.grid(row=12,column=4,pady=25,padx=25)
        canvas.mainloop()
        label2.after(600,Loop)
        #root.quit()
    else:
        label1.configure(text=results[1])
        label2.configure(text=results[2])
        print(maincounter)
        dreamer(maincounter)#Calling the dreamer function by the id in the database
        time.sleep(15)
        #myimg=ImageTk.PhotoImage(Image.open(results[3]))#change the image path
        #imagine.configure(image=myimg)#change the label
        #imagine.grid(row=6,column=6,pady=25,padx=25)
        #image.after(200,imageLoop)#recursion to keep changing.
        cursor2=mydb.cursor()
        sql3=('use tiktoksd')
        cursor2.execute(sql3)
        sql4=('select * from data where id=%s')
        data4=(maincounter,)
        cursor2.execute(sql4,data4)
        resultsNew=cursor2.fetchone()
        maincounter+=1#incrementing the global counter
        #label1.after(200,Loop)
        #label2.configure(image=myimg)
        #imagine.after(600,Loop)
        cur_path=resultsNew[3]
        pil_img=Image.open(cur_path).resize((500, 500))
        myimg=ImageTk.PhotoImage(pil_img)#change the image path
        canvas.itemconfigure(imageContainer,image=myimg)
        canvas.grid(row=12,column=4,pady=25,padx=25)
        canvas.mainloop()
        label2.after(600,Loop)
        #root.quit()
        #canvas.after(200,Loop)
            



unique_id=input("Please enter the account name:")
image_path=cur_path
AutoRefresh()
refresh_image(canvas,img,image_path,imageContainer)
#unique_id='ifoodsuk'
t1=threading.Thread(target=tiktokapi,args=(unique_id,))
t1.start()
root.mainloop()

#Loop()

        
        
    

    

    
    
    
    


