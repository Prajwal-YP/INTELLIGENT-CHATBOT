import exp as YPtool
import tkinter as tk
# import ttkbootstrap as ttk
from PIL import ImageTk, Image
import tkcalendar as tkc


main = tk.Tk()

# MAIN WINDOW TITLE
main.title("YP-Chatbot")
main['background']="#DCD03E"
icon = ImageTk.PhotoImage(Image.open(r"D:\8TH SEMISITER\project\proof\logo.png"))
main.iconphoto(False,icon)

# MAIN HEADING LABEL
l1=tk.Label(main,text="C H A T B O T        A P P L I C A T I O N")
l1.grid(row=0,column=0,padx=90,pady=30)
l1.configure(background='#DCD03E',foreground="#cc3380",font="rockwell 20 bold")


# MAIN WINDOW BODY
def setup(ans,frame=None):
    if frame:
        frame.destroy()
    
    frame = tk.Frame(main, width=0, height=400)
    frame.grid(row=2, column=0,columnspan=3, padx=10, pady=5)
    frame['background']="#DCD03E"
    
    e={}
    l={}
    b={}
    
    if ans=='sign_up':
        ele = ['NAME','GENDER','DOB','EMAIL','PASSWORD','REPEAT_PASSWORD']

        for i in range(len(ele)):
 
            # INSERT LABELS FOR SIGN_UP PAGE 
            l[ele[i]]=tk.Label(frame,text=ele[i])
            l[ele[i]].grid(row=i,column=0,sticky='w',pady=7)
            l[ele[i]].configure(font='Times_New_Roman 9')
            
            #INSERT ELEMENTS FRO SIGN_UP PAGE
            if ele[i]=="DOB":
                e[ele[i]]=tkc.DateEntry(frame,width=40)
                e[ele[i]].grid(row=i,column=1,padx=20,columnspan=2)
                continue
            if ele[i]=="GENDER":
                GENDER= tk.IntVar()
                e[ele[i]]=tk.Radiobutton(frame,text="Male",variable=GENDER,value=0)
                e[ele[i]].grid(row=i,column=1,padx=20,columnspan=2)
                e[ele[i]]=tk.Radiobutton(frame,text="Female",variable=GENDER,value=1)
                e[ele[i]].grid(row=i,column=2,padx=20,columnspan=2)
                e[ele[i]]=GENDER
                continue

            e[ele[i]]=tk.Entry(frame)
            e[ele[i]].grid(row=i,column=1,padx=20,columnspan=2)
            e[ele[i]].config(width=42)

        # INSERT BUTTONS FOR SIGN_UP PAGE 

        b[ans]=tk.Button(frame,text=ans,command=lambda:YPtool.register(ele,e,setup,frame))
        b[ans].grid(row=7,column=2)
        b['Already have account?']    = tk.Button(frame,text="Already have account?",command=lambda:setup("sign_in",frame))
        b['Already have account?'].grid(row=8,column=1)

        # DESIGN LABELS IN SIGN_UP PAGE 
        for i in l:
            l[i]['bg']='#DCD03E'

        # DESIGN BUTTONS IN SIGN_UP PAGE
        for i in b:
            b[i]['background']          = '#cccaff'
            b[i]['foreground']          = '#20a100'
            b[i]['activebackground']    = "#DCD03E"
            b[i]['activeforeground']    = '#cc9900'
            b[i]['border']              = 3
            b[i]['borderwidth']         = 5
            b[i]['cursor']              = 'star'
            b[i]['font']                = 'Rockwell','13' 
            YPtool.changeOnHover(b[i],"#20a100","#cccaff")
    elif ans=='sign_in':
        ele = ['EMAIL','PASSWORD']
        # pic = ImageTk.PhotoImage(Image.open('./proof/logo.png'))
        # l2 = tk.Label(main, image = pic)
        # l2.grid(row=0,column=0)
        
        # LABEL AND ELEMENT CREATION FOR SIGN_IN
        for i in range(len(ele)):
            l[ele[i]]=tk.Label(frame,text=ele[i])
            l[ele[i]].grid(row=i,column=0,sticky='w',pady=7)
            l[ele[i]].config(font='Times_New_Roman 9')
            e[ele[i]]=tk.Entry(frame)
            e[ele[i]].grid(row=i,column=1,padx=20,columnspan=2)
            e[ele[i]].config(width=42)

        # BUTTON CREATION FOR SIGN_IN
        b[ans] = tk.Button(frame,text=ans,command=lambda:YPtool.authorize(e,main))
        b[ans].grid(row=6,column=2)
        b["face recognize"]=tk.Button(frame,text="face recognize",command=lambda:YPtool.face_authorize(e,main))
        b['face recognize'].grid(row=6,column=0)
        b['Create new account?'] = tk.Button(frame,text="Create new account?",command=lambda:setup("sign_up",frame))
        b['Create new account?'].grid(row=7,column=1)

        #LABEL DESIGN
        for i in l:
            l[i]['bg']='#DCD03E'
        
        # BUTTON DESIGN
        for i in b:
            b[i]['background']          = '#cccaff'
            b[i]['foreground']          = '#20a100'
            b[i]['activebackground']    = "#DCD03E"
            b[i]['activeforeground']    = '#cc9900'
            b[i]['border']              = 3
            b[i]['borderwidth']         = 5
            b[i]['cursor']              = 'star'
            b[i]['font']                = 'Rockwell','13' 
            YPtool.changeOnHover(b[i],"#20a100","#cccaff")
    return frame

frame = setup('sign_in')

# MAIN WINDOW DIPLAY LOOP
main.mainloop()





# YPtool.take_pics(num_itr=5,takes=4)
# YPtool.VERIFY()
# YPtool.analyse()