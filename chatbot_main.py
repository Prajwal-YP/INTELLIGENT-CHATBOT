import tkinter as tk
import chatbot,os,pyttsx3
import playsound,pyautogui,time
import gtts
from datetime import datetime 
from exp import analyse

current_datetime = datetime.now()
current_date    = current_datetime.date()
current_datetime = datetime.now().time()  
current_minute  = current_datetime.strftime("%M")
current_second  = current_datetime.strftime("%S")
current_time=str(current_date)+str(current_minute)+str(current_second)

def do_save():
    # Handle the "Save" command
    txt=chatWindow.get("1.0", tk.END)
    
    fn='D:\\8TH SEMISITER\\project\\chatHistory\\'+str(current_time)+'.txt'
    file = open(fn,'w')
    file.write(txt)

def simle_please():
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.typewrite('camera')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.hotkey('win','r')
    pyautogui.typewrite('cmd')
    pyautogui.press('enter')
    time.sleep(1.5)
    pyautogui.typewrite("ECHO \"SMILE PLEASE DUDE \"")
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite("exit")
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('up')
    pyautogui.press('up')
    pyautogui.press('down')
    pyautogui.press('space')

def record_me():
    pyautogui.press('win')
    time.sleep(.8)
    pyautogui.typewrite('camera')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.hotkey('win','r')
    pyautogui.typewrite('cmd')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite("cls & ECHO \"BE READY FOR 10 SECOND VIDEO \"")
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.typewrite("exit")
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('up')
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('space')
    time.sleep(11) 
    pyautogui.press('space')



import tkinter as tk

root = tk.Tk()
root.title("Chatbot")

# Create the menu bar
menu_bar = tk.Menu(root)    

# Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
# file_menu.add_command(label="New", command=lambda:do_new(chatWindow))
file_menu.add_command(label="Save", command=do_save)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Attach the menu bar to the root window
root.config(menu=menu_bar)

# img=Image.new('RGBA',(500,500),(1,3,2,10))

# Set background color
root.configure(bg="#214323")
root.geometry("480x580")

# Set fonts
font_style = ("Arial Rounded MT Bold", 10)
font_style_button = ("Arial Rounded MT Bold", 12)

# Create chat window
chatWindow = tk.Text(root, bd=2,bg="grey", height="18", width="9000", font=font_style)
chatWindow.config(state=tk.DISABLED,padx=1,pady=1,height=10)


# Create message window
var=tk.StringVar()
messageWindow = tk.Entry(root, bd=1, bg="#f2f2f2",textvariable=var)

def engine(var,chatWindow,messageWindow):
    txt=var.get()
    if txt.isspace() or txt=='':
        return
    else:
        inp=txt.strip()
        txt = "You: "+inp+'\n'
        print(txt)
        
        chatWindow.configure(state='normal')
        chatWindow.insert('end',txt+'\n')
        ans=chatbot.chat(inp)
        txt= "YP_BOT: "+ans[0]+'\n'
        chatWindow.insert('end',txt+'\n')
        chatWindow.configure(state='disabled')
        try:
            os.remove("welcome.mp3")
        except:
            pass
        try:
            sound=gtts.gTTS(ans[0],lang='en')
            sound.save('welcome.mp3')
            playsound.playsound('welcome.mp3')
        except:
            pass
        messageWindow.insert('0','')
        print(ans)
        if ans[1]=='pic':
            simle_please()
        if ans[1]=='video':
            record_me()
        if ans[1]=='face':
            pyautogui.hotkey('win','r')
            pyautogui.typewrite('cmd')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.typewrite('D:')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.typewrite('cd 8TH SEMISITER/project')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.typewrite("python -c \"import exp; exp.analyse()\"")
            pyautogui.press('enter')
        # del e


# Create send button
sendButton = tk.Button(root, text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b", font=font_style_button,command=lambda:engine(var,chatWindow,messageWindow))

# Place all components on the screen
chatWindow.place(x=28, y=6, height=386, width=390)
messageWindow.place(x=198, y=400, height=88, width=265)
sendButton.place(x=6, y=400, height=88)

root.mainloop()