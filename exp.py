from deepface import DeepFace
import matplotlib.pylab as plt
from tkinter import messagebox
import pandas as pd
import cv2,time,os,re,string,random,shutil
import tkinter as tk

def take_pics(email,num_itr,takes):
    # delete unwanted pics
    emails = os.listdir('./images')
    user_path = './images/'+email
    if email in emails:
        shutil.rmtree(user_path)
    os.mkdir(user_path)

    try:
        for i in range(num_itr):
            cam = cv2.VideoCapture(0)   # 0 -> index of camera
            print(user_path)
            for j in range(takes):
                s,img = cam.read()
                cv2.imwrite(user_path+'/'+str(j+(i*takes))+".jpg",img)
            cam.release()
        return 1
    except:
        return 0

def VERIFY(email,unknown_images,known_images,win):

    # Path to store unknown face
    pth = './img/'

    # capture ad save unknwon faces
    cam = cv2.VideoCapture(0) 
    for i in range(3):
        s,img = cam.read()
        cv2.imwrite(pth+str(i)+".jpg",img)
    cam.release()

    # store the path names of known and unknown images in lists
    known=[]
    unknown=[]

    for i in range(unknown_images):
        unknown.append(pth+str(i)+".jpg")
    pth = './images/'+email+'/'     # Known images path
    for i in range(known_images):
        known.append(pth+str(i)+".jpg")

    # Verify whether the unknown pics match any of the known pics 
    value=[]    # store verification result in value list
    for i in known:
        for j in unknown:
            res = DeepFace.verify(img1_path=i,img2_path=j)
            value.append(res["verified"])
    # print("\n",value)
    
    # Match condition
    ans = 0
    for i in value:
        if i: ans+=1
    threshold=(len(value)/2)-(len(value)/20)

    if ans>threshold:
        messagebox.showinfo("SIGN_UP","Face match")
        win.destroy()
        os.system('python chatbot_main.py')
    else:
        messagebox.showerror("SIGN_UP","Face not match")

    # delete unwanted pics
    shutil.rmtree('./img')
    os.makedirs('./img')

def analyse():
    pth =r"D:\8TH SEMISITER\project\img"
    print("Be Ready in 5 seconds !!")
    time.sleep(3)
    cam = cv2.VideoCapture(0)
    status,image = cam.read()
    cam.release()
    pth += '\\image.jpg'
    cv2.imwrite(pth,image)


    # Face Extraction
    face_objs = DeepFace.extract_faces(img_path=pth)

    # Face Analysis 
    objs = DeepFace.analyze( img_path = pth, actions = ['age', 'gender', 'race', 'emotion'],)
    time.sleep(10)

    print(objs[0]['age'])
    print(objs[0]['gender'])
    print(objs[0]['emotion'])

    print('success')

    gender  = objs[0]['dominant_gender']
    race    = objs[0]['dominant_race']
    emotion = objs[0]['dominant_emotion']
    print(objs[0])

    print(gender,race,emotion)
    # Face Presentation
    fig,ax = plt.subplots(2,2,figsize=(20,8),gridspec_kw={'width_ratios':[4,3]})
    d=objs[0]
    ax[0,0].imshow(face_objs[0]['face'])
    x=d['gender'].keys()
    y=d['gender'].values()
    ax[0,1].bar(x,y)
    x=d['race'].keys()
    y=d['race'].values()
    ax[1,0].bar(x,y)
    x=d['emotion'].keys()
    y=d['emotion'].values()
    ax[1,1].bar(x,y) 

    # PLOTTING FIGURES AND SETTING TITLE 
    title=f"FACIAL ANALYSIS\nrace:{race}  Gender:{gender}  emotion:{emotion}"
    fig.suptitle(title)
    plt.subplots_adjust(left=0.027,
                    bottom=0.111,
                    right=0.995,
                    top=0.92,
                    wspace=0.062,
                    hspace=0.183)
    plt.show()

    # TRUNCATING UNWANTED TEMPORARY IMAGE 
    os.system("D:")
    cmd = r''' del D:\8TH SEMISITER\project\img /q '''
    os.system(cmd)

def changeOnHover(button, colorOnHover, colorOnLeave):
    # background on entering widget
    button.bind("<Enter>", func=lambda e: button.config(background=colorOnHover,foreground=colorOnLeave))
    # background color on leving widget
    button.bind("<Leave>", func=lambda e: button.config(background=colorOnLeave,foreground=colorOnHover))

def verify_account(required_string):
    ERROR=[]
    if is_user_present(required_string['EMAIL'])!=False:
        ERROR.append('EMAIL ALREADY EXISTS, SIGN IN !!')
        return ERROR
    if required_string["NAME"]=='':
        ERROR.append("ENTER YOUR NAME !!")
    res = re.search("^(.*)@(.*)(\..*$){1,2}",required_string["EMAIL"])
    if res==None:
        ERROR.append("ENTER PROPER EMAIL !!")
    p1=required_string["PASSWORD"]
    p2=required_string["REPEAT_PASSWORD"]
    if p1.isspace() or p1=='':
        ERROR.append("ENTER PASSWORD !!")
    if p1!=p2:
        ERROR.append("ENTER SAME in PASSWORD and REPEAT_PASSWORD !!")
    if ',' in p1:
        ERROR.append("PASSWORD CAN NOT CONTAIN , !!")
    return ERROR

def encrypt(key,password):
        encrypted_password  = ''
        reference           = list(''+string.punctuation+string.digits+string.ascii_letters)
        reference.remove(',')
        for i in password:
            encrypted_password += key[reference.index(i)]
        return encrypted_password

def decrypt(key,encrypted_password):
        decrypted_password  = ''
        reference           = list(''+string.punctuation+string.digits+string.ascii_letters)
        reference.remove(',')
        for i in encrypted_password:
            decrypted_password += reference[key.index(i)]
        return decrypted_password

def register(ele,e,setup,frame):
    required_string = {}

    # COLLECT VALUES FROM  SIGN_UP PAGE TO REQUIRED STRING DICTIONARY
    for i in ele:
        if i=='GENDER':
            if e[i].get()==0:
                required_string[i]='Male'
            else:
                required_string[i]='Female'
            continue
        if i=='PASSWORD' or i=="REPEAT_PASSWORD":
            required_string[i] = e[i].get()
            continue
        required_string[i] = (e[i].get().lower()).strip()
    
    # PERFORM AUTHENTICATION FOR ALL DETAILS
    AUTHENTICATION=verify_account(required_string)
    
    if(AUTHENTICATION==[]):     # NO ERRORS
        password            = required_string['PASSWORD']
        reference           = list(''+string.punctuation+string.digits+string.ascii_letters)
        reference.remove(',')
        key                 = reference.copy()
        random.shuffle(key)

        # ENCRYPT THE PASSWORD USING KEY
        encrypted_password  = encrypt(key,password)
        required_string['PASSWORD']=encrypted_password
        del required_string['REPEAT_PASSWORD']

        content = list(required_string.values())
        content = ','.join(content)
        
        # STORE USER DETAILS AND KEYS IN RESPECTIVE FILES
        file = open("users.txt",'a')
        file.write(content+"\n")
        file.close()

        content=required_string['EMAIL']+'->'+str(key)
        file = open("keys.txt",'a')
        file.write(content+'\n')
        file.close()

        messagebox.showinfo('Face_Recognition',"BE READY TO REGISTER YOUR FACE\n1. BRING FACE CLOSER TO CAMERA\n2. MAKE SURE YOUR PLACE HAVE GOOD LIGHTING\n3. PIC WILL BE TAKEN 5 TIMES (five captures)\n  READY ?")
        ans = take_pics(required_string['EMAIL'],5,3)
        while ans==0:
            messagebox.showerror("FACE REGOCNITION",'RECOGITION FAILED!!'+"\n1. BRING FACE CLOSER TO CAMERA\n2. MAKE SURE YOUR PLACE HAVE GOOD LIGHTING\n3. PIC WILL BE TAKEN 5 TIMES (five captures)\n  READY ?")
            ans = take_pics(required_string['EMAIL'],5,3)
        messagebox.showinfo("SIGN_UP","SUCCESSFUL.")    
        setup("sign_in",frame)

    else:                       # ERRORS IN DETAILS
        error=''
        for i in AUTHENTICATION:
            error += i +'\n'
        
        # DISPLAY ALL ERRORS IN MESSAGEBOX
        messagebox.showerror('SIGN_UP ERROR', error)

def is_user_present(email):
    ele=("NAME","GENDER","DOB","EMAIL","PASSWORD")

    # CHECK IF USER EXISTS AND GET ENCRYPTED PASSWORD 
    try:
        df = pd.read_csv('users.txt',names=ele)
        emails = list(df['EMAIL'])
        row_search = emails.index(email)
    except:
        return False
    encrypted_password = df.iloc[row_search,4]
    print(encrypted_password)
    return encrypted_password

def is_user_authorized(email,password,encrypted_password):
    # DECRYPT THE ENCRYPTED PASSWORD 
    file = open('keys.txt')
    decrypted_password=''
    for line in file:
        pattern = '^(.*)->(.*)$'
        ans=re.findall(pattern,line)
        if(ans[0][0]==email):
            key = eval(ans[0][1])
            decrypted_password = decrypt(key,encrypted_password)
            break
    file.close()

    # CHECK WHETHER PASSWORD AND DECRYPTED PASSWORD WORKS
    if password == decrypted_password:
        return True
    else:
        return False

def authorize(e,win):
    email = (e["EMAIL"].get().lower()).strip()
    password = e["PASSWORD"].get()
    encrypted_password = is_user_present(email)
    AUTHENTICATION = is_user_authorized(email,password,encrypted_password)
    if email=="":
        AUTHENTICATION=False
    if AUTHENTICATION:
        messagebox.showinfo("SIGN_IN","SUCCESSFUL")
        win.destroy()
        os.system('python chatbot_main.py')

    else:
        messagebox.showerror("SIGN_IN","INVALID EMAIL / PASSWORD")

def face_authorize(e,main):
    email = (e["EMAIL"].get().lower()).strip()
    if email.isspace() or email=='':
        messagebox.showerror("SIGN_IN","ENTER EMAIL !!")
        return
    AUTHENTICATION = is_user_present(email)

    if AUTHENTICATION!=False:
        VERIFY(email,3,15,main)
    else:
        messagebox.showerror("SIGN_IN","INVALID EMAIL")

# analyse()