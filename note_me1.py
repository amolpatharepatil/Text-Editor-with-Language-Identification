import tkinter as tk
from tkinter import Frame, Grid, Image, PhotoImage, Scrollbar, Text, ttk,font
from tkinter import font,colorchooser,filedialog,messagebox
import os
from tkinter.constants import BOTTOM, FALSE, NONE, TOP, TRUE
from matplotlib import colors
import pandas as pd
import numpy as np
import re
import pickle
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import warnings
from statistics import mode
from sklearn.metrics import accuracy_score, confusion_matrix

warnings.simplefilter("ignore")

os.chdir("/Users/aniketabhale/Downloads/ai")
le = LabelEncoder()
data = pd.read_csv("/Users/aniketabhale/Downloads/ai/Language Detection.csv")
# value count for each language
data["Language"].value_counts()
# separating the independent and dependant features
X = data["Text"]
y = data["Language"]
# converting categorical variables to numerical
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)
# creating a list for appending the preprocessed text
data_list = []
# iterating through all the text
for text in X:
    # removing the symbols and numbers
    text = re.sub(r'[!@#$(),n"%^*?:;~`0-9]', ' ', text)
    text = re.sub(r'[[]]', ' ', text)
    # converting the text to lower case
    text = text.lower()
    # appending to data_list
    data_list.append(text)
# creating bag of words using countvectorizer
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(data_list).toarray()
def predict(text):
    Pkl_Filename = "/Users/aniketabhale/Downloads/ai/Pickle_RL_Model.pkl" 
    with open(Pkl_Filename, 'rb+') as file:  
        Pickled_LR_Model = pickle.load(file)
        x = cv.transform([text]).toarray()
        lang = Pickled_LR_Model.predict(x)
        lang = le.inverse_transform(lang)
    return lang

main_swasher=tk.Toplevel()
main_swasher.geometry('1200x900')
main_swasher.title("Text-Editor")

#"note_me\\atomwriter icon\\new .png"
#**************part1*********
main_menu=tk.Menu()
#**************part1*********
#images taken for file menu


#code for file menu
#new button functionality
data_main=""
def new_main_func(event=None):
    global data_main
    data_main=""
    text_editor_main.delete(1.0,tk.END)

#New File
file=tk.Menu(main_menu,tearoff=False)
file.add_command(label="New",compound=tk.LEFT,accelerator="ctrl+N",command=new_main_func)


def open_file_main(event=None):#open file functionality
    global data_main 
    data_main = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
    try:
        with open(data_main, 'r') as fr:
            text_editor_main.delete(1.0, tk.END)
            text_editor_main.insert(1.0, fr.read())
    except FileNotFoundError:
        return 
    except:
        return 
    main_swasher.title(os.path.basename(data_main))
file.add_command(label="open",compound=tk.LEFT,accelerator="ctrl+o",command=open_file_main)
#save file functionality
def save_file_main(event=None):
    global data_main
    try:
        if data_main:
            writtendata=str(text_editor_main.get(1.0,tk.END))
            with open(data_main,"w",encoding="utf-8") as file3:
                file3.write(writtendata)
        else:
            data_main=filedialog.asksaveasfile(mode="w",defaultextension="txt",filetypes=(("Text files","*.txt"),("All files","*.*")))
            writtendata2=text_editor_main.get(1.0,tk.END)
            data_main.write(writtendata2)
            data_main.close()
    except:
        return
file.add_command(label="save",compound=tk.LEFT,accelerator="ctrl+s",command=save_file_main)
def save_as_main(event=NONE):
    global data_main
    try:
        if data_main:
            data_main=filedialog.asksaveasfile(mode="w",defaultextension="txt",filetypes=(("Text files","*.txt"),("All files","*.*")))
            writtendata2=text_editor_main.get(1.0,tk.END)
            data_main.write(writtendata2)
            data_main.close()
    except:
        return
file.add_command(label="save as",compound=tk.LEFT,accelerator="ctrl+alt+s",command=save_as_main)
text_changed=True
def exit_func(event=None):
    global data_main, text_changed
    try:
        if text_changed:
            mbox = messagebox.askyesnocancel('Warning', 'Do you want to save the file ?')
            if mbox is True:
                if data_main:
                    content = text_editor_main.get(1.0, tk.END)
                    with open(data_main, 'w', encoding='utf-8') as fw:
                        fw.write(content)
                        main_swasher.destroy()
                else:
                    content2 = str(text_editor_main.get(1.0, tk.END))
                    data_main = filedialog.asksaveasfile(mode = 'w', defaultextension='.txt', filetypes=(('Text File', '*.txt'), ('All files', '*.*')))
                    data_main.write(content2)
                    data_main.close()
                    main_swasher.destroy()
            elif mbox is False:
                main_swasher.destroy()
        else:
            main_swasher.destroy()
    except:
        return 
file.add_command(label="exit",compound=tk.LEFT,accelerator="ctrl+d",command=exit_func)


#code for edit menu
edit=tk.Menu(main_menu,tearoff=False)

edit.add_command(label="copy",compound=tk.LEFT,accelerator="ctrl+c",command=lambda:text_editor_main.event_generate("<Control c>"))
edit.add_command(label="paste",compound=tk.LEFT,accelerator="ctrl+v",command=lambda:text_editor_main.event_generate("<Control v>"))
edit.add_command(label="cut",compound=tk.LEFT,accelerator="ctrl+x",command=lambda:text_editor_main.event_generate("<Control x>"))
edit.add_command(label="clear all",compound=tk.LEFT,accelerator="ctrl+Alt+x",command=lambda:text_editor_main.delete(1.0,tk.END))



#all cascade
main_menu.add_cascade(label="File",menu=file)
main_menu.add_cascade(label="Edit",menu=edit)
main_swasher.config(menu=main_menu)
#*************************************part2------->fontbox,sizebox,boldbutton,italic button,underline button,fontcolor button
#**fontset,leftalign button,centeraligh button,rightalign button ---->all mounted on status bar

tool_bar=ttk.Label(main_swasher)
tool_bar.pack(side=tk.TOP,fill=tk.X)

font_set=tk.font.families()
font_save=tk.StringVar()
font_box=ttk.Combobox(tool_bar,width=25,textvariable=font_save,state="readonly")
font_box["values"]=font_set
font_box.current(font_set.index('Arial'))
font_box.grid(column=0,row=0,pady=5)#padx is to move right with desired value to move



#size box
size_box_data=tk.IntVar()
size_box_area=ttk.Combobox(tool_bar,width=10,textvariable=size_box_data,state="readonly")
size_box_area["value"]=list(range(4,200,2))
size_box_area.grid(column=1,row=0,padx=5)
size_box_area.set(11)
#bold button
bold_button=ttk.Button(tool_bar,width=5,text="Bold")
bold_button.grid(column=2,row=0,pady=5)
#italic button
italic_button=ttk.Button(tool_bar,width=5,text="Italic")
italic_button.grid(column=3,row=0,pady=5)
#underline button
underline_button=ttk.Button(tool_bar,text="Underline")
underline_button.grid(column=4,row=0,pady=5)

#leftalign button
left_button=ttk.Button(tool_bar,width=5,text="Left")
left_button.grid(column=6,row=0,pady=5)
#centeralign button
center_button=ttk.Button(tool_bar,text="Center")
center_button.grid(column=7,row=0,pady=5)
#rightalign button
right_button=ttk.Button(tool_bar,width=5,text="Right")
right_button.grid(column=8,row=0,pady=5)

pri_button=ttk.Button(tool_bar,text="Identify")
pri_button.grid(column=9,row=0,pady=5)

pri_label=ttk.Label(tool_bar,text="-- IDENTIFIED LANGUAGE --")

pri_label.grid(column=10,row=0,pady=5)

#*****************part3---------->text editor**************


#text editor and scroll bar
text_editor_main=tk.Text(main_swasher)
text_editor_main.config(wrap="word",relief=tk.FLAT)

Scrollbar_main=Scrollbar(main_swasher)
text_editor_main.focus_set()
Scrollbar_main.pack(side=tk.RIGHT,fill=tk.Y)
text_editor_main.pack(fill=tk.BOTH,expand=TRUE)
Scrollbar_main.config(command=text_editor_main.yview)
text_editor_main.config(yscrollcommand=Scrollbar_main.set)
#font bindining
current_font_data="Arial"
current_font_size_data=14
#func for font type
def font_jump(main_swasher):
    global current_font_data
    current_font_data=font_save.get()
    text_editor_main.configure(font=(current_font_data,current_font_size_data))
font_box.bind("<<ComboboxSelected>>", font_jump)
#func for font size and fuctionality
def font_size_jump(main_swasher):
    global current_font_size_data
    current_font_size_data=size_box_data.get()
    text_editor_main.configure(font=(current_font_data,current_font_size_data))
size_box_area.bind("<<ComboboxSelected>>", font_size_jump)
     
text_editor_main.configure(font=("Arial",14))# it will print by default data in arialand size will be 14

'''
this print statement will print the output as below list 
print(tk.font.Font(font=text_editor_main["font"]).actual())
output={'family': 'Arial', 'size': 14, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
and for bold button we need to access the weight element of list,similarly u caon use slant for italic and underline 
for making underline text 
''' 
''''''


def make_bold():
    current_tags = text_editor_main.tag_names("sel.first")
    if "bt" in current_tags:
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        text_editor_main.tag_remove("bt", "sel.first", "sel.last")
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
    else:
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        text_editor_main.tag_add("bt", "sel.first", "sel.last")
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        
bold_button.configure(command=make_bold)
#for italic button
'''def italic_making():
    italic_texting=tk.font.Font(font=text_editor_main["font"])
    if italic_texting.actual()["slant"]=="roman":
        text_editor_main.configure(font=(current_font_data,current_font_size_data,"italic"))
    if italic_texting.actual()["slant"]=="italic":
        text_editor_main.configure(font=(current_font_data,current_font_size_data,"normal"))   
  '''      
def make_italic():
    current_tags = text_editor_main.tag_names("sel.first")
    if "it" in current_tags:
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        text_editor_main.tag_remove("it", "sel.first", "sel.last")
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
    else:
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        text_editor_main.tag_add("it", "sel.first", "sel.last")
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
italic_button.configure(command=make_italic)

#for underline button
'''def underline_making():
    underline_texting=tk.font.Font(font=text_editor_main["font"])
    if underline_texting.actual()["underline"]==0:
        text_editor_main.configure(font=(current_font_data,current_font_size_data,"underline"))
    if underline_texting.actual()["underline"]==1:
        text_editor_main.configure(font=(current_font_data,current_font_size_data,"normal"))    
'''
def make_underline():
    current_tags = text_editor_main.tag_names("sel.first")
    if "ut" in current_tags:
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        text_editor_main.tag_remove("ut", "sel.first", "sel.last")
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
    else:
        text_editor_main.configure(font=(current_font_data,current_font_size_data))
        text_editor_main.tag_add("ut", "sel.first", "sel.last")
        text_editor_main.configure(font=(current_font_data,current_font_size_data))


underline_button.configure(command=make_underline)


#left alignment
def left_text_alignment_making():
    main_text_data=text_editor_main.get(1.0,"end")
    text_editor_main.tag_config("left",justify=tk.LEFT)
    text_editor_main.delete(1.0,tk.END)
    text_editor_main.insert(tk.INSERT,main_text_data,"left")
left_button.configure(command=left_text_alignment_making)

#center alignment
def center_text_alignment_making():
    main_text_data=text_editor_main.get(1.0,"end")
    text_editor_main.tag_config("center",justify=tk.CENTER)
    text_editor_main.delete(1.0,tk.END)
    text_editor_main.insert(tk.INSERT,main_text_data,"center")
center_button.configure(command=center_text_alignment_making)
#right alignment
def right_text_alignment_making():
    main_text_data=text_editor_main.get(1.0,"end")
    text_editor_main.tag_config("right",justify=tk.RIGHT)
    text_editor_main.delete(1.0,tk.END)
    text_editor_main.insert(tk.INSERT,main_text_data,"right")
right_button.configure(command=right_text_alignment_making)

def prid():
    main_text_data=text_editor_main.get(tk.SEL_FIRST,tk.SEL_LAST)
    print(main_text_data)
    pri_label.config(text="    "+mode(predict(main_text_data)),foreground='blue',font=("Helvetica", 18,'bold'))
   
    print(mode(predict(main_text_data)))
    
    
pri_button.configure(command=prid)

bold_font = font.Font(text_editor_main, text_editor_main.cget("font"))
bold_font.configure(weight="bold")
text_editor_main.tag_configure("bt", font=bold_font)

italic_font = font.Font(text_editor_main, text_editor_main.cget("font"))
italic_font.configure(slant="italic")
text_editor_main.tag_configure("it", font=italic_font)

underline_font = font.Font(text_editor_main, text_editor_main.cget("font"))
underline_font.configure(underline="1")
text_editor_main.tag_configure("ut", font=underline_font)

text_editor_main.bind("<Control-n>", new_main_func)
text_editor_main.bind("<Control-o>", open_file_main)
text_editor_main.bind("<Control-s>", save_file_main)
text_editor_main.bind("<Control-Alt-s>", save_as_main)
text_editor_main.bind("<Control-q>", exit_func)
main_swasher.mainloop()