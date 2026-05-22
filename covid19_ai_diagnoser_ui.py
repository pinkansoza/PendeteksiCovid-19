#Author: Jordan Bennett
#Modern UI Update
import covid19_ai_diagnoser

from tkinter import Frame, Tk, BOTH, Label, Menu, filedialog, messagebox, Text
from PIL import Image, ImageTk

import os
import codecs
import cv2

screenWidth = "1200"
screenHeight = "800"
windowTitle = "Smart/Ai Coronavirus 2019 (Covid19) Diagnosis Tool"

class Window(Frame):
    _PRIOR_IMAGE = None
    DIAGNOSIS_RESULT = ""
    DIAGNOSIS_RESULT_FIELD = None

    def __init__(self, master=None):
        Frame.__init__(self, master, bg="#1E1E2E")
        self.master = master
        self.pack(fill=BOTH, expand=1)
        
        # Title
        self.title_label = Label(self, text="AI COVID-19 & Pneumonia Diagnoser", bg="#1E1E2E", fg="#89B4FA", font=("Segoe UI", 28, "bold"))
        self.title_label.place(relx=0.5, rely=0.08, anchor="center")

        # Subtitle
        self.subtitle_label = Label(self, text="Smart CT-Scan & X-Ray Analysis Tool", bg="#1E1E2E", fg="#A6ADC8", font=("Segoe UI", 12))
        self.subtitle_label.place(relx=0.5, rely=0.14, anchor="center")

        try:
            load = Image.open("covid19_ai_diagnoser_default__.jpg")
            load = load.resize((480, 480), getattr(Image, 'Resampling', Image).LANCZOS)
        except Exception:
            # Create a blank placeholder if image is missing
            load = Image.new("RGB", (480, 480), color="#313244")

        render = ImageTk.PhotoImage(load)
        
        # Image border frame
        self.img_frame = Frame(self, bg="#45475A", bd=0)
        self.img_frame.place(relx=0.5, rely=0.48, anchor="center")
        
        img = Label(self.img_frame, image=render, bg="#1E1E2E", padx=5, pady=5)
        img.image = render
        img.pack(padx=2, pady=2)
        
        self._PRIOR_IMAGE = self.img_frame
        
        self.DIAGNOSIS_RESULT_FIELD = Text(self, width=100, height=8, bg="#181825", fg="#CDD6F4", 
                                           font=("Consolas", 12), relief="flat", padx=20, pady=20, 
                                           insertbackground="#CDD6F4", highlightthickness=1, highlightbackground="#313244", highlightcolor="#89B4FA")
        self.DIAGNOSIS_RESULT_FIELD.place(relx=0.5, rely=0.86, anchor="center")
        
    def addDiagnosisResult(self, value):
        self.DIAGNOSIS_RESULT_FIELD.delete("1.0", "end")
        self.DIAGNOSIS_RESULT = ""
        self.DIAGNOSIS_RESULT_FIELD.insert("1.0", value)


root = Tk()
app = Window(root)
root.configure(bg="#1E1E2E")

root.wm_title(windowTitle)
root.geometry(f"{screenWidth}x{screenHeight}")

menubar = Menu(root, bg="#181825", fg="#CDD6F4", activebackground="#89B4FA", activeforeground="#11111B", relief="flat")

filemenu = Menu(menubar, tearoff=0, bg="#181825", fg="#CDD6F4", activebackground="#89B4FA", activeforeground="#11111B", font=("Segoe UI", 10))
menubar.add_cascade(label=" 📁 Analysis Options ", menu=filemenu)

CONSTANT_DIAGNOSIS_IMAGE_SPAN = 480

def loadRegularPneumoniaImageFromDialog():
    currdir = os.getcwd()
    image_file = filedialog.askopenfile(mode='r', parent=root, initialdir=currdir, title='Select X-Ray Image (Regular Pneumonia):')
    if image_file:
        root.wm_title(windowTitle + " - " + image_file.name)
        loadRegularPneumoniaImageFromName(image_file.name)

def loadRegularPneumoniaImageFromName(filename):
    app._PRIOR_IMAGE.destroy() 
    load = Image.open(filename)
    load = load.resize((CONSTANT_DIAGNOSIS_IMAGE_SPAN, CONSTANT_DIAGNOSIS_IMAGE_SPAN), getattr(Image, 'Resampling', Image).LANCZOS)
    render = ImageTk.PhotoImage(load)
    
    img_frame = Frame(app, bg="#89B4FA", bd=0) # Blue border for regular pneumonia
    img_frame.place(relx=0.5, rely=0.48, anchor="center")
    
    img = Label(img_frame, image=render, bg="#1E1E2E")
    img.image = render
    img.pack(padx=3, pady=3)
    
    app.DIAGNOSIS_RESULT += "--- NON-COVID19 MODE ---\nTarget: " + filename + "\n\n"
    app.DIAGNOSIS_RESULT += covid19_ai_diagnoser.doOnlineInference_regularPneumonia(filename)
    print(app.DIAGNOSIS_RESULT)
    
    app._PRIOR_IMAGE = img_frame 
    app.addDiagnosisResult(app.DIAGNOSIS_RESULT)
    enableDiagnosisResultColouring()
    
def loadCovid19ImageFromDialog():
    currdir = os.getcwd()
    image_file = filedialog.askopenfile(mode='r', parent=root, initialdir=currdir, title='Select X-Ray Image (COVID-19):')
    if image_file:
        root.wm_title(windowTitle + " - " + image_file.name)
        loadCovid19ImageFromName(image_file.name)

def loadCovid19ImageFromName(filename):
    app._PRIOR_IMAGE.destroy() 
    load = Image.open(filename)
    load = load.resize((CONSTANT_DIAGNOSIS_IMAGE_SPAN, CONSTANT_DIAGNOSIS_IMAGE_SPAN), getattr(Image, 'Resampling', Image).LANCZOS)
    render = ImageTk.PhotoImage(load)
    
    img_frame = Frame(app, bg="#F38BA8", bd=0) # Red border for COVID mode
    img_frame.place(relx=0.5, rely=0.48, anchor="center")
    
    img = Label(img_frame, image=render, bg="#1E1E2E")
    img.image = render
    img.pack(padx=3, pady=3)
    
    app.DIAGNOSIS_RESULT += "--- COVID19 MODE ---\nTarget: " + filename + "\n\n"
    app.DIAGNOSIS_RESULT += covid19_ai_diagnoser.doOnlineInference_covid19Pneumonia(filename)
    print(app.DIAGNOSIS_RESULT)
    
    app._PRIOR_IMAGE = img_frame 
    app.addDiagnosisResult(app.DIAGNOSIS_RESULT)
    enableDiagnosisResultColouring()

filemenu.add_command(label="🔬 Test Image for Regular Pneumonia", command=loadRegularPneumoniaImageFromDialog)
filemenu.add_separator()
filemenu.add_command(label="🦠 Test Image for COVID-19", command=loadCovid19ImageFromDialog)

def colourDiagnosisMessageText(diagnosisContent, startIndexText, endIndexText):
    # If pneumonia or covid19 is detected
    if (covid19_ai_diagnoser.DIAGNOSIS_MESSAGES[0] in diagnosisContent or covid19_ai_diagnoser.DIAGNOSIS_MESSAGES[1] in diagnosisContent):
        app.DIAGNOSIS_RESULT_FIELD.tag_add("DIAGNOSIS_RESULT_MESSAGE", startIndexText, endIndexText)
        app.DIAGNOSIS_RESULT_FIELD.tag_configure("DIAGNOSIS_RESULT_MESSAGE", background="#F38BA8", foreground="#11111B", font=("Consolas", 12, "bold"))

    # If normal lungs state is detected
    if (covid19_ai_diagnoser.DIAGNOSIS_MESSAGES[2] in diagnosisContent):
        app.DIAGNOSIS_RESULT_FIELD.tag_add("DIAGNOSIS_RESULT_MESSAGE", startIndexText, endIndexText)
        app.DIAGNOSIS_RESULT_FIELD.tag_configure("DIAGNOSIS_RESULT_MESSAGE", background="#A6E3A1", foreground="#11111B", font=("Consolas", 12, "bold"))

def enableDiagnosisResultColouring():
    diagnosisResultFieldContent = app.DIAGNOSIS_RESULT_FIELD.get("1.0", "end")
    colourDiagnosisMessageText(diagnosisResultFieldContent, "4.0", "4.21")

root.config(menu=menubar)
root.mainloop()
