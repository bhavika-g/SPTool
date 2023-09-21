
import csv
from email.mime import image
import matplotlib
matplotlib.use('TkAgg')
from tkinter import *
from tkinter import filedialog
from tkinter import ttk as ttk

import DataRead as DR
import DataAnalyze as DA
import GenFolderStruct as GFS
import shutil
import DataAnalysisCode as DAC

import numpy as np

import os.path
from PIL import ImageTk, Image

import tkinter.font as font
from tkinter import messagebox
import customtkinter

import DataAnalysisCode_cross as DACC

"""========================================================================================"""

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class MainScreen:
    
    def __init__(self):
        
     root1= Tk()
     root1.title(" ")
     
     root1.geometry("659x685")
     #root1.eval('tk::PlaceWindow . center')
     #root1.resizable(width=False, height=False)
     root1.configure(bg= "#99CBBB")
     center(root1)
     screen_img= PhotoImage(file="widgets/brain.png")
     my_label= Label(image=screen_img)
     my_label.place(x=0, y=0)
     
     frame1= Frame(root1)
     frame1.pack(pady=70)

     myFont = font.Font(size=22)

     self.a3 = Button(frame1, text= "Synapse Tool", borderwidth=0, command= lambda: self.MainWindowButton(), height= 2, width=10)
     self.a3.pack(pady=60)
     self.a1 = Button(frame1, text= "Tutorials", borderwidth=0, height= 2, width=10)
     self.a1.pack(pady=60)

     self.a2 = Button(frame1, text= "FAQs", borderwidth=0, height= 2, width=10)
     self.a2.pack(pady= 60)

     self.a1['font']= myFont
     self.a2['font']= myFont
     self.a3['font']= myFont
    #  self.optionmenu_1 = customtkinter.CTkOptionMenu(master= frame1, values=["Light", "Dark", "System"], command=self.change_appearance_mode)
    #  self.optionmenu_1.pack()

     

     mainloop()

    def MainWindowButton(self):
     root= Toplevel()
     win= MainWindow(root)

    def change_appearance_mode(self, new_appearance_mode):
     customtkinter.set_appearance_mode(new_appearance_mode)





class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 1000     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
    



class MainWindow(Frame):

     def __init__(self, root):
        
    #   root1= Tk()
    #   root1.geometry("659x685")
    #   root1.eval('tk::PlaceWindow . center')
    #   root1.resizable(width=False, height=False)
    #   #root1.configure(bg= "#99CBBB")
    #   screen_img= PhotoImage(file="widgets/brain.png")
    #   self.my_label= Label(image=screen_img)
    #   self.my_label.grid(row=0, column=0, columnspan=5)
 
    #   self.a1 = Button(text= "Tutorials", borderwidth=0)
    #   self.a1.grid(row=1,column=0,padx=0, pady=0)

    #   self.a2 = Button(text= "FAQs", borderwidth=0)
    #   self.a2.grid(row=2,column=0,padx=0, pady= 0)

    #   root = Toplevel()

    #   self.a3 = Button(text= "Synapse Tool", borderwidth=0, command= lambda: self.mw(self, root))
    #   self.a3.grid(row=0,column=1,padx=0, pady=0)

    #   mainloop()

    #  def mw(self, root):
        """Generate the main selection screen of the Synapse tool"""
        
        global read_data_img
        global choose_dir_img
        global gen_fol_img
        global anal_data_img
        global clr_data_img 

        self.root= root
        
        self.frame= Frame(self.root)
        root.title("Synapse Tool")
       # root.eval('tk::PlaceWindow . center')
        root.geometry("580x500")
        center(root)
        #root.configure(bg= "#99CBBB")
        root.resizable(width=False, height=False)

        self.folder_path = ""
        
        #images
        read_data_img= PhotoImage(file="widgets/read.png")
        choose_dir_img= PhotoImage(file="widgets/dir.png")
        #choose_dir_img.zoom(200,200)
        gen_fol_img= PhotoImage(file="widgets/gen.png")
        anal_data_img= PhotoImage(file="widgets/stats.png")

        clr_data_img= PhotoImage(file="widgets/clear.png")

       # self.b1 = Button(text="Choose Directory", command=self.browse_button)
        self.b1 = Button(root, text= "Choose Directory", image= choose_dir_img, compound= TOP, command=self.browse_button, borderwidth=0)
        self.b1.grid(row=0,column=1, padx=30, pady=30)

        b1_ttp = CreateToolTip(self.b1, 'Choose the directory we will consider')

        self.l1 = Label(root, text = self.folder_path,bg="#DCE4EF", width=20, height=1) # borderwidth=2)
        self.l1.grid(row=1,column=1,padx=30, pady=30)

        self.bGenDat = Button(root, text= "Read Data", image= read_data_img, compound= TOP, command =lambda:self.GenData_button(), borderwidth=0) 
        self.bGenDat.grid(row=2,column=1,padx=30, pady=30)

        bGen_ttp = CreateToolTip(self.bGenDat, 'Construct data from experimental data')

        #self.bAnDat = Button(text="Analyze data", command=lambda:self.AnalData_button())
        self.bAnDat = Button(root, text="Analyze Data", image=anal_data_img, compound= TOP, command=lambda:self.AnalData_button(), borderwidth=0)
        self.bAnDat.grid(row=2,column=2,padx=30, pady=30)

        bAn_ttp = CreateToolTip(self.bAnDat, 'Analyze generated data')

        self.bDirStruct = Button(root, text="Generate Folders", image=gen_fol_img,compound= TOP, command = lambda:self.DirStruct_button(), borderwidth=0)
        self.bDirStruct.grid(row=2,column=0,padx=30, pady=30)

        bDir_ttp = CreateToolTip(self.bDirStruct, 'Transform the data to the correct structure')

        self.bClearDat = Button(root, text="Clear Data", image=clr_data_img, compound= TOP, command=lambda:self.CleanData_button(), borderwidth=0)
        self.bClearDat.grid(row=3,column=1,padx=30, pady=30)

        bGen_ttp = CreateToolTip(self.bClearDat, 'Clear directory for a fresh restart')

        #root.wm_transient(root1)

       # mainloop()

     def browse_button(self):
        """Function that sets the desired folder"""

        filename = filedialog.askdirectory()
        Dir =str(filename)

        self.l1.config(text="Folder: " + Dir)
        self.folder_path = str(filename)

     def GenData_button(self):
        """Function that generates the read data window"""

        root2 = Toplevel()
        app2 = GenerateWindow(root2,self.folder_path)

     def AnalData_button(self):
        """Function that generates the anaylze data window"""

        # #try:
        # Acceptable = []
        # tdict      = {}

        # for c in sorted(os.listdir(self.folder_path)):
        #     cellType = os.path.split(self.folder_path)[-1]

        #     if(os.path.exists(self.folder_path+'/'+c+'/Synapses'+cellType+'_'+c+".csv")):
        #         xall = [x if ((x[-3:]=='lsm') or (x[-3:]=='tif')) else '' for x in os.listdir(self.folder_path+'/'+c)]
        #         lenTime = len(list(filter(('').__ne__, xall)))
        #         Acceptable.append(c+'/')

        #         # Check if the cells were stimulated so that this can be flagged to the user
        #         SynCSV = self.folder_path+'/'+c+'/Synapses'+cellType+'_'+c+".csv"

        #         with open(SynCSV, newline='') as f:

        #             reader = csv.reader(f)
        #             row = np.array([float(x) for x in next(reader)])
        #             tdict[c] = self.CheckDat(row,lenTime)

        # root4 = Toplevel()
        # app4 = DataAnalyzeWindow(root4,self.folder_path)
        self.plt_window = Toplevel()
        self.plt_window.geometry("1000x700") #460x350
        center(self.plt_window)
        
        my_notebook = ttk.Notebook(self.plt_window)
        my_notebook.grid(pady=15)

        spatial_frame= Frame(my_notebook)
        temporal_frame= Frame(my_notebook)
        #custom_frame= Frame(my_notebook, width=1000, height= 700)


        spatial_frame.grid(padx=15, pady=15)
        temporal_frame.grid(padx=15, pady=15)

        #top_frame = Frame(spatial_frame, bg='cyan', width=450, height=50, pady=3)
        centr = Frame(spatial_frame, bg='white', width=950, height=390, padx=3, pady=3, highlightbackground="gray", highlightthickness=1)
        btm_frame = Frame(spatial_frame, bg='white', width=950, height=40, pady=3, highlightbackground="gray", highlightthickness=1)
        btm_frame2 = Frame(spatial_frame, bg='#CBF9E7', width=950, height=180, pady=3, highlightbackground="gray", highlightthickness=1)

# layout all of the main containers
        spatial_frame.grid_rowconfigure(1, weight=1)
        spatial_frame.grid_columnconfigure(0, weight=1)

        #top_frame.grid(row=0, sticky="ew")
        centr.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        btm_frame2.grid(row=4, sticky="ew")

        # model_label = Label(top_frame, text='Model Dimensions')
        # width_label = Label(top_frame, text='Width:')
        # length_label = Label(top_frame, text='Length:')
        # entry_W = Entry(top_frame, background="pink")
        # entry_L = Entry(top_frame, background="orange")

# layout the widgets in the top frame
        # model_label.grid(row=0, columnspan=3)
        # width_label.grid(row=1, column=0)
        # length_label.grid(row=1, column=2)
        # entry_W.grid(row=1, column=1)
        # entry_L.grid(row=1, column=3)

        centr.grid_rowconfigure(0, weight=1)
        centr.grid_columnconfigure(1, weight=1)

        self.ctr_left = Frame(centr, bg='#CBF9E7', width=300, height=390)
       
        ctr_mid = Frame(centr, bg='white', width=250, height=390, padx=3, pady=3)
        #ctr_right = Frame(centr, bg='green', width=100, height=190, padx=3, pady=3)

        self.ctr_left.grid(row=0, column=0, sticky="ns")
        
        ctr_mid.grid(row=0, column=1, sticky="nsew")
        #ctr_right.grid(row=0, column=2, sticky="ns")
        #custom_frame.grid(row=0, column=0)
        self.ctr_left_in= Frame(self.ctr_left, bg='#CBF9E7', width=300, height=250)
        self.ctr_left_in.grid(row=4, column=0, sticky="ns")

        title_label = Label(btm_frame2, text='Plot Title')
        x_label = Label(btm_frame2, text='X-Axis Label')
        y_label = Label(btm_frame2, text='Y-Axis Label')


        title_label.grid(row=0, column=0, padx=30)
        
        x_label.grid(row=2, column=0, padx=30)
        y_label.grid(row=4, column=0, padx=30)

        self.x_label_entry= StringVar()
        self.y_label_entry= StringVar()
        self.plot_title_entry= StringVar()


        self.entry_title = Entry(btm_frame2, textvariable = self.plot_title_entry, background="white")
        self.entry_x = Entry(btm_frame2, textvariable = self.x_label_entry, background="white")
        self.entry_y = Entry(btm_frame2, textvariable = self.y_label_entry, background="white")
        custom_button= Button(btm_frame2, text="Custom Plot")
        # entry_L = Entry(top_frame, background="orange")

        self.folder_path_analysis = ""

        self.entry_title.grid(row=1, column=0, pady=5, padx=30)
        self.entry_x.grid(row=3, column=0, pady=5, padx=30)
        self.entry_y.grid(row=5, column=0, pady=5, padx=30)
        #custom_button.grid(row=5, column=1, pady=10, sticky= 'se')

        choose_dir_button= Button(self.ctr_left,text="Choose Directory", command=self.browse_button_2)
        self.dir_entry= Label(self.ctr_left, text = self.folder_path_analysis, bg="white", width=20, height=1)
        
        plot_option= customtkinter.CTkOptionMenu(master= self.ctr_left, values=["Spine Area [Histogram]", "Spine Clustering [C-means]", "Spine Clustering [K-means]", "Spine Intensity vs Time [Heatmap]"], command=self.check_boxes)
        plot_option.set("") 

        choose_dir_button.grid(row=0, pady=10, padx=30)
        self.dir_entry.grid(row=1, pady=10, padx=30)
        
        plot_option.grid(row=3, pady=10, padx=30)

        self.customise_plot= Label(btm_frame, bg="white", width=20, height=1, text= 'Customise Plot')
        self.customise_plot.config(font=('Helvatical bold',14))
        self.customise_plot.place(x=475, y= 15, anchor= 'center')

        # self.check_box_1 = customtkinter.CTkCheckBox(master=ctr_left, text="Display Error Bar", text_color= 'black')
        # self.check_box_2 = customtkinter.CTkCheckBox(master=ctr_left, text="Display Mean", text_color= 'black')
        # self.check_box_3 = customtkinter.CTkCheckBox(master=ctr_left, text="Display Median", text_color= 'black')
        # self.check_box_4 = customtkinter.CTkCheckBox(master=ctr_left, text="Display Standard Error", text_color= 'black')
        # self.check_box_1.grid(row=4, pady=10, padx=30)
        # self.check_box_2.grid(row=5, pady=10, padx=30)
        # self.check_box_3.grid(row=6, pady=10, padx=30)
        # self.check_box_4.grid(row=7, pady=10, padx=30)

        go_button= Button(btm_frame2,text="Go!", command= self.set_choice)
        go_button.grid(row=1, column= 1, pady=10, padx=30) 




        ###### Cross Experiment Window ######

        centr_2 = Frame(temporal_frame, bg='white', width=950, height=390, padx=3, pady=3, highlightbackground="gray", highlightthickness=1)
        btm_frame_2 = Frame(temporal_frame, bg='white', width=950, height=40, pady=3, highlightbackground="gray", highlightthickness=1)
        btm_frame2_2 = Frame(temporal_frame, bg='#CBF9E7', width=950, height=180, pady=3, highlightbackground="gray", highlightthickness=1)

        # layout all of the main containers
        temporal_frame.grid_rowconfigure(1, weight=1)
        temporal_frame.grid_columnconfigure(0, weight=1)

        #top_frame.grid(row=0, sticky="ew")
        centr_2.grid(row=1, sticky="nsew")
        btm_frame_2.grid(row=3, sticky="ew")
        btm_frame2_2.grid(row=4, sticky="ew")


        centr_2.grid_rowconfigure(0, weight=1)
        centr_2.grid_columnconfigure(1, weight=1)

        self.ctr_left_2 = Frame(centr_2, bg='#CBF9E7', width=300, height=390)
       
        self.ctr_mid_2 = Frame(centr_2, bg='white', width=250, height=390, padx=3, pady=3)
        #ctr_right = Frame(centr, bg='green', width=100, height=190, padx=3, pady=3)

        self.ctr_left_2.grid(row=0, column=0, sticky="ns")
        
        self.ctr_mid_2.grid(row=0, column=1, sticky="nsew")
        #ctr_right.grid(row=0, column=2, sticky="ns")
        #custom_frame.grid(row=0, column=0)
        self.ctr_left_in_2= Frame(self.ctr_left_2, bg='#CBF9E7', width=300, height=250)
        self.ctr_left_in_2.grid(row=4, column=0, sticky="ns")

        title_label_2 = Label(btm_frame2_2, text='Plot Title')
        x_label_2 = Label(btm_frame2_2, text='X-Axis Label')
        y_label_2 = Label(btm_frame2_2, text='Y-Axis Label')


        title_label_2.grid(row=0, column=0, padx=30)
        
        x_label_2.grid(row=2, column=0, padx=30)
        y_label_2.grid(row=4, column=0, padx=30)

        self.x_label_entry_2= StringVar()
        self.y_label_entry_2= StringVar()
        self.plot_title_entry_2= StringVar()


        self.entry_title_2 = Entry(btm_frame2_2, textvariable = self.plot_title_entry, background="white")
        self.entry_x_2 = Entry(btm_frame2_2, textvariable = self.x_label_entry, background="white")
        self.entry_y_2 = Entry(btm_frame2_2, textvariable = self.y_label_entry, background="white")
        custom_button_2= Button(btm_frame2_2, text="Custom Plot")
        # entry_L = Entry(top_frame, background="orange")

        self.folder_path_analysis_2 = ""

        self.entry_title_2.grid(row=1, column=0, pady=5, padx=30)
        self.entry_x_2.grid(row=3, column=0, pady=5, padx=30)
        self.entry_y_2.grid(row=5, column=0, pady=5, padx=30)
        #custom_button.grid(row=5, column=1, pady=10, sticky= 'se')

        # choose_dir_button_2= Button(self.ctr_left_2,text="Choose Directory", command=self.browse_button_2)
        # self.dir_entry_2= Label(self.ctr_left_2, text = self.folder_path_analysis_2, bg="white", width=20, height=1)
        
        

        #choose_dir_button_2.grid(row=0, pady=10, padx=30)
        #self.dir_entry_2.grid(row=1, pady=10, padx=30)
        
        #plot_option_2.grid(row=3, pady=10, padx=30)

        self.customise_plot_2= Label(btm_frame_2, bg="white", width=20, height=1, text= 'Customise Plot')
        self.customise_plot_2.config(font=('Helvatical bold',14))
        self.customise_plot_2.place(x=475, y= 15, anchor= 'center')

    

        go_button_2= Button(btm_frame2_2,text="Go!", command= self.set_choice_2)
        go_button_2.grid(row=1, column= 1, pady=10, padx=30) 




        self.number_of_datasets= Label(self.ctr_left_2, text = "Enter Number of Datasets")
        self.number_of_datasets.grid(row=0, padx=10, pady=10)



       # self.l2_1= Label(self.master, text = "[Enter 1 for a single experiment analysis or >1 for cross experiment analysis]",bg="#DCE4EF", width=40, height=5)
       # self.l2_1.grid(row=1, column=0, padx=20, pady=20)
        self.Enter_box= Entry(self.ctr_left_2)
        self.Enter_box.grid(row=1, padx= 20, pady=10)
        enter_box_tip= CreateToolTip(self.Enter_box, 'Enter number of datasets/experiments [=<5]' )

        enter_button= Button(self.ctr_left_2, text = "Enter", command= self.verify)
        enter_button.grid(row=2, padx=10, pady=10)



        self.my_button= {}
        self.my_entry= {}













        my_notebook.add(spatial_frame, text="Single Experiment")
        my_notebook.add(temporal_frame,text= "Cross Experiment")




     def verify(self):
        for widget in self.ctr_mid_2.winfo_children():
             widget.destroy()
        try:
            int(self.Enter_box.get())
            self.input_num= int(self.Enter_box.get())
            self.dir_list= []
            self.var=0
            for x in range(self.input_num):
          
                self.my_entry[x]= Label(self.ctr_mid_2, height=1, width=20)
                self.my_entry[x].grid(row=x+3, column=0, padx=20, pady=5)
                self.my_button[x]= Button(self.ctr_mid_2, text = "Choose Directory", command=lambda:self.dir_button(x, self.dir_list))
                self.my_button[x].grid(row=x+3, column=1, padx=5, pady=5) 
            plot_option_2= customtkinter.CTkOptionMenu(master= self.ctr_left_2, values=["Spine Density[Bar-Graph]", "Average Spine Area[Line Graph]", "Average Spine Area[Bar Graph]"], command=self.check_boxes_2)
            plot_option_2.set("Select Graph") 
            plot_option_2.grid(row=3)
            warning_label= Label(self.ctr_mid_2, height=4, width=50, text= "**Make sure to re-name the directory containing \n the .json file with the desired Dataset/Experiment Name** \n For example, to name a Dataset/Experiment as 'Control_1', \n the path should be ''/Users/xxx/Folder/Images/Control_1/Synapse_l.json'' ", bg='white')
            warning_label.grid(row= self.input_num+4 )

        
            
            #self.graph_button= Button(self.master, text="Move to Analysis", command= self.move_to_anal)
            #self.graph_button.grid(row=self.input_num+1, column= 2, padx=10, pady=20)
            
        except ValueError:
            messagebox.showerror('Enter an integer value!')

     
     
     
     def dir_button(self, x, dir_list):
        """Function that sets the desired folder and creates an array for all the directories"""
        
        filename = filedialog.askdirectory()
        Dir =str(filename)
        self.dir_list.append(Dir)
    
        self.my_entry[self.var].config(text="Folder: " + Dir)
        self.var= self.var+1
     
     def browse_button_2(self):
        """Function that sets the desired folder"""

        filename = filedialog.askdirectory()
        Dir =str(filename)

        self.dir_entry.config(text="Folder: " + Dir)
        self.folder_path_analysis = str(filename)

     def set_choice(self):
         #print(choice)
         n=1
         path= self.folder_path_analysis


         median= self.output[1]
         mean= self.output[2]
         std= self.output[3]
         kde= self.output[4]
         clusters= self.output[5]
         choice= self.output[0]
         x_axis= self.x_label_entry.get()
         y_axis= self.y_label_entry.get()
         plot_title= self.plot_title_entry.get()

         

         do= DAC.Plots(path, n, choice, median, mean, std, kde, clusters, x_axis, y_axis, plot_title) 

     def set_choice_2(self): #path, x_label, y_label, plot_title, dataset_name, um_pixel, pixel_size, median, mean, std_err, error_bars, legend
         #print(choice)
         
         Dir_Arr= self.dir_list 
         x_label= self.x_label_entry_2.get()
         y_label= self.y_label_entry_2.get()
         plot_title= self.plot_title_entry_2.get()
         um_pixel= self.output_2[1]
         pixel_size= self.output_2[2]
         median= self.output_2[3]
         mean= self.output_2[4]
         std_err= self.output_2[5]
         error_bars= self.output_2[6]
         legend= self.output_2[7]
         choice= self.output_2[0]
         

         do= DACC.Plots(choice, Dir_Arr, x_label, y_label, plot_title, um_pixel, pixel_size, median, mean, std_err, error_bars, legend) 

     def check_boxes(self, choice):
         self.output= []
         if (choice== "Spine Area [Histogram]"): #median, mean, std, kde, clusters 
          for widget in self.ctr_left_in.winfo_children():
             widget.destroy()
          self.kde_var = StringVar(self.ctr_left_in, "on")
          self.mean_var = StringVar(self.ctr_left_in, "on")
          self.std_var = StringVar(self.ctr_left_in, "on")
          self.median_var = StringVar(self.ctr_left, "on")
          self.check_box_1 = customtkinter.CTkCheckBox(master=self.ctr_left_in, text="Display KDE", text_color= 'black', variable=self.kde_var, onvalue="on", offvalue="off")
          self.check_box_2 = customtkinter.CTkCheckBox(master=self.ctr_left_in, text="Display Mean", text_color= 'black', variable=self.mean_var, onvalue="on", offvalue="off")
          self.check_box_3 = customtkinter.CTkCheckBox(master=self.ctr_left_in, text="Display Median", text_color= 'black', variable=self.median_var, onvalue="on", offvalue="off")
          self.check_box_4 = customtkinter.CTkCheckBox(master=self.ctr_left_in, text="Display Standard Error", text_color= 'black', variable=self.std_var, onvalue="on", offvalue="off")
          #self.stat_option= customtkinter.CTkOptionMenu(master= self.ctr_left, values=['count','frequency', 'probability', 'proportion', 'percent', 'density'])
        #   self.stat_option.set("") 
        #   self.stat_option.grid(row=4, pady=10, padx=30)
          self.check_box_2.grid(row=0, pady=10, padx=30)
          self.check_box_3.grid(row=1, pady=10, padx=30)
          self.check_box_4.grid(row=2, pady=10, padx=30)
          self.check_box_1.grid(row=3, pady=10, padx=30)
          self.output= [choice, self.median_var, self.mean_var, self.std_var, self.kde_var, "False"]


         if (choice== "Spine Clustering [C-means]"): #self, title, clusters #median, mean, std, kde, clusters 
          for widget in self.ctr_left_in.winfo_children():
             widget.destroy()   

          title_label = Label(self.ctr_left_in, text='Set Number of Clusters')
          title_label.grid(row=0, pady=10, padx=30)
          self.slider_value= []
          self.slider = customtkinter.CTkSlider(master=self.ctr_left_in, from_=0, to=10, command=self.slider_event) 
          self.slider.grid(row=1, pady=10, padx=30)
          self.output= [choice, "False", "False", "False", "False", self.slider_value ]
         
         
         if (choice== "Spine Clustering [K-means]"): #self, clusters, title #median, mean, std, kde, clusters 
          for widget in self.ctr_left_in.winfo_children():
             widget.destroy()
          title_label = Label(self.ctr_left_in, text='Set Number of Clusters')
          title_label.grid(row=0, pady=10, padx=30)
          self.slider_value= []
          self.slider = customtkinter.CTkSlider(master=self.ctr_left_in, from_=0, to=10, command=self.slider_event) 
          self.slider.grid(row=1,pady=10, padx=30)
          self.output= [choice, "False", "False", "False", "False", self.slider_value]

         if (choice== "Spine Intensity vs Time [Heatmap]"): #self, clusters, title #median, mean, std, kde, clusters 
           for widget in self.ctr_left_in.winfo_children():
             widget.destroy()

           self.output= [choice, "False", "False", "False", "False", "False"]


            


         #if (choice== "Spine Intensity vs Time [Heatmap]"): #self, title, x_label, y_label

        

        
       # my_notebook.add(custom_frame,text= "Custom Analysis")


        #except:
        #    alert_popup("Warning","Oops - something went wrong")

     def check_boxes_2(self, choice): #self, x_label, y_label, plot_title, dataset_name, um_pixel, pixel_size, median, mean, std_err, error_bars, legend
         self.output= []
         if (choice== "Spine Density[Bar-Graph]"):  #um/pixel, pixel size, xlabel, ylabel, title, mean, median, std, error_bars, legend
          for widget in self.ctr_left_in_2.winfo_children():
             widget.destroy()

          self.err_var = StringVar(self.ctr_left_in_2, "on")
          self.mean_var = StringVar(self.ctr_left_in_2, "on")
          self.std_var = StringVar(self.ctr_left_in_2, "on")
          self.median_var = StringVar(self.ctr_left_2, "on")
          self.legend_var = StringVar(self.ctr_left_2, "on")

          self.check_box_1 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Error Bars", text_color= 'black', variable=self.err_var, onvalue="on", offvalue="off")
          self.check_box_2 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Mean", text_color= 'black', variable=self.mean_var, onvalue="on", offvalue="off")
          self.check_box_3 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Median", text_color= 'black', variable=self.median_var, onvalue="on", offvalue="off")
          self.check_box_4 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Standard Error", text_color= 'black', variable=self.std_var, onvalue="on", offvalue="off")
          self.check_box_5 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Legend", text_color= 'black', variable=self.legend_var, onvalue="on", offvalue="off")
          self.label_um= Label(self.ctr_left_in_2, text= "Enter \u03BCm per pixel" ).grid(row=3, column=0, pady=10, padx=30 )
          self.entry_um= Entry(self.ctr_left_in_2)
          self.label_pixel= Label(self.ctr_left_in_2, text= "Enter number of pixels in image" ).grid(row=4, column=0, pady=10, padx=30 )
          self.entry_pixel= Entry(self.ctr_left_in_2)
          self.entry_pixel.grid(row=4, column=1, pady=10, padx=30)
          self.entry_um.grid(row=3,column=1, pady=10, padx=30)


          #self.stat_option= customtkinter.CTkOptionMenu(master= self.ctr_left, values=['count','frequency', 'probability', 'proportion', 'percent', 'density'])
        #   self.stat_option.set("") 
        #   self.stat_option.grid(row=4, pady=10, padx=30)
          self.check_box_2.grid(row=0, column=0, pady=10, padx=30)
          self.check_box_3.grid(row=1, column=0, pady=10, padx=30)
          self.check_box_4.grid(row=2, column=0,pady=10, padx=30)
          self.check_box_1.grid(row=0, column=1, pady=10, padx=30)
          self.check_box_5.grid(row=1, column=1, pady=10, padx=30 )

          if(self.entry_pixel.get()):
              entry_pixel= self.entry_pixel.get()

          else:
              entry_pixel= 1204

          if(self.entry_um.get()):
              entry_um= self.entry_um.get()

          else:
              entry_um= 0.66

       
          self.output_2= [choice, entry_um, entry_pixel, self.median_var, self.mean_var, self.std_var, self.err_var, self.legend_var]


         if (choice== "Average Spine Area[Line Graph]"): #xlabel, ylabel, title, error_bars, legend
          for widget in self.ctr_left_in_2.winfo_children():  #self, x_label, y_label, plot_title, dataset_name, um_pixel, pixel_size, median, mean, std_err, error_bars, legend
            
            widget.destroy()   
            
          self.err_var = StringVar(self.ctr_left_in_2, "on")
          self.legend_var = StringVar(self.ctr_left_2, "on")
          self.check_box_1 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Error Bars", text_color= 'black', variable=self.err_var, onvalue="on", offvalue="off")
          self.check_box_5 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Legend", text_color= 'black', variable=self.legend_var, onvalue="on", offvalue="off")
          self.check_box_1.grid(row=0, pady=10, padx=30)
          self.check_box_5.grid(row=1,pady=10, padx=30 )
          
          self.output_2= [choice, 0, 0, "False", "False", "False", self.err_var, self.legend_var]
         
         
         if (choice== "Average Spine Area[Bar Graph]"): #xlabel, ylabel, title, error_bars, legend 

          for widget in self.ctr_left_in_2.winfo_children():  #self, x_label, y_label, plot_title, dataset_name, um_pixel, pixel_size, median, mean, std_err, error_bars, legend
            
            widget.destroy()   

          self.err_var = StringVar(self.ctr_left_in_2, "on")
          self.legend_var = StringVar(self.ctr_left_2, "on")
          self.check_box_1 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Error Bars", text_color= 'black', variable=self.err_var, onvalue="on", offvalue="off")
          self.check_box_5 = customtkinter.CTkCheckBox(master=self.ctr_left_in_2, text="Display Legend", text_color= 'black', variable=self.legend_var, onvalue="on", offvalue="off")
          self.check_box_1.grid(row=0, pady=10, padx=30)
          self.check_box_5.grid(row=1,pady=10, padx=30 )
          
          self.output_2= [choice, 0, 0, "False", "False", "False", self.err_var, self.legend_var]


        
     def CheckDat(self,row1,lenTime):

        """Flag that passes whether the normalized data was a success"""

        temp = row1[4:lenTime+4]-row1[-2*lenTime:-lenTime]
        temp2 = temp[3]/np.nanmean(temp[:3])

        # 1 and 1.2 are chosen relatively arbitrary and can be changed
        if(temp2<1):
            check = 2
        elif(temp2<1.2):
            check = 1
        else:
            check = 0

        return check

     def slider_event(value):
         self.slider_value= value 
    

     def CleanData_button(self):
        """Function that generates the clean data window"""
        root3 = Toplevel()
        app3 = DeleteWindow(root3,self.folder_path)

     def DirStruct_button(self):
        """Function that generates the directory generation window"""
        root5 = Toplevel()
        app5 = DirStructWindow(root5)

     

     
      

"""========================================================================================"""

class DirStructWindow:
    """Class that defines the directory structure window"""
    def __init__(self,master):

        self.master = master
        self.frame = Frame(self.master)

        self.source_path = ""
        self.target_path = ""

        self.b1 = Button(master,text="Choose source directory", command=self.source_button)
        self.b1.grid(row=0,column=0,padx=5, pady=5)

        self.l1 = Label(master, text = self.source_path,bg="light blue")
        self.l1.grid(row=1,column=0,padx=5, pady=5)


        self.b2 = Button(master,text="Choose target directory", command=self.target_button)
        self.b2.grid(row=0,column=1,padx=5, pady=5)

        self.l2 = Label(master, text = self.target_path,bg="light blue")
        self.l2.grid(row=1,column=1,padx=5, pady=5)

        self.l3 = Label(master, text = 'New folder name:')
        self.l3.grid(row=2,column=0,padx=5, pady=5)

        self.e1 = Entry(master,width=10)
        self.e1.grid(row=2,column=1,padx=5, pady=5)

        self.progress = ttk.Progressbar(master, orient = HORIZONTAL, length = 100, mode = 'determinate')
        self.progress.grid(row=3,column=0,padx=5, pady=5)

        self.bgo     = Button(master,text="Go!", command=self.go_button)
        self.bgo.grid(row=3,column=1,padx=5, pady=5)

    def source_button(self):
        """ Allow user to select a directory and store it in global var called source_path """

        filename = filedialog.askdirectory()
        Dir =str(filename)
        self.l1.config(text="Folder: " + os.path.split(Dir)[-1])
        self.source_path = str(filename)

    def target_button(self):
        """ Allow user to select a directory and store it in global var called target_path """

        filename = filedialog.askdirectory()
        Dir =str(filename)
        self.l2.config(text="Folder: " + os.path.split(Dir)[-1])
        self.target_path = str(filename)

    def go_button(self):
        """ Generate the target directory, and deleting the directory if it already exists"""
        try:
            GFS.CreateCellDirs(self.source_path,self.target_path,self.e1.get(),self)
        except:
            self.deleteDir_popup()

    def deleteDir_popup(self):
        """ Window that gives users last chance to rethink if they really want to delete the files and
        send them to the nether realm"""
        root = Toplevel()
        root.title('Warning!')

        m = 'Do you want to delete ' + self.e1.get() + '? \n There might be files in it.'
        w = Label(root, text=m)
        w.grid(row=0,column=0,padx=5, pady=5)
        b1 = Button(root, text="OK", command=lambda:self.DeleteDir(root), width=10)
        b1.grid(row=1,column=0,padx=5, pady=5)

        b2 = Button(root, text="Cancel", command=root.destroy, width=10)
        b2.grid(row=1,column=1,padx=5, pady=5)

    def DeleteDir(self,root):
        """ It's done - the files will be deleted."""
        if(os.path.exists(self.target_path+'/'+self.e1.get())):
            shutil.rmtree(self.target_path+'/'+self.e1.get())
            root.destroy()

"""========================================================================================"""

class GenerateWindow(Frame):
    def __init__(self,master,Dir):

        """Class that defines the read data window"""

        self.master = master
        self.frame = Frame(self.master)
        self.master.configure(bg= "#99CBBB")



        self.Dir   = Dir
        self.v = StringVar()

        self.MC = IntVar()

        Label(master, text="Select synapse data").grid(row = 0, column = 0)

        self.Proj = StringVar(master)
        self.Proj.set('Max')
        choices2 = sorted({ "Sum","Max","Min","Mean","Median","None"})
        self.ProjMen = OptionMenu(master, self.Proj, *choices2)
        self.ProjMen.grid(row = 0, column = 2)
        Zp_ttp = CreateToolTip(self.ProjMen, 'z-projection')

        self.Mode = StringVar(master)
        self.Mode.set('Luminosity')
        choices = sorted({ "Area","Luminosity","Soma","Puncta","Dendrite"})
        self.zpMenu = OptionMenu(master, self.Mode, *choices)
        self.zpMenu.grid(row = 1, column =2)
        pZ_ttp = CreateToolTip(self.zpMenu, 'Select if you want to measure area or Luminosity')
    

        self.e1 = Entry(master,width=5)
        self.e1.grid(row=3,column=1,padx=5, pady=5)

        e1_ttp = CreateToolTip(self.e1, 'Enter the first cell you want to anaylze')

        self.e2 = Entry(master,width=5)
        self.e2.grid(row=3,column=2,padx=5, pady=5)

        self.e3 = Entry(master,width=5)
        self.e3.grid(row=1,column=1,padx=5, pady=5)
        Label(master, text="\u03BCm per pixel").grid(row = 0, column = 1)

        self.chk = Checkbutton(master, text='Multi-channel', variable=self.MC)
        self.chk.grid(row=1,column=0,padx=5, pady=5)

        e2_ttp = CreateToolTip(self.e2, 'Enter the last cell you want to analyze')

        Label(master, text="Cells").grid(row = 3, column = 0)

        self.progress = ttk.Progressbar(master, orient = HORIZONTAL, length = 100, mode = 'determinate')
        self.progress.grid(row=5,column=0,padx=5, pady=5)

        self.l1 = Label(master, textvariable=self.v,bg="white",width=40)
        self.l1.grid(row=5,column=1,padx=5, pady=5)

        self.b1 = Button(master,text="Go!",command = self.Gen_button)
        self.b1.grid(row=6,column=1,padx=5, pady=5)

        self.b2= Button(master,text="Clear",command = self.clearlab)
        self.b2.grid(row=5,column=2,padx=5, pady=5)

        b2_ttp = CreateToolTip(self.b2, 'Clear the textfield')

    def close_windows(self):
        self.master.destroy()

    def clearlab(self):
        self.v.set("")

    def Gen_button(self):
        # Allow user to select a directory and store it in global var
    # called folder_path
        #try:
        if(self.e2.get()==""):
            a = int(self.e1.get())
        else:
            a = int(self.e2.get())

        if(self.e3.get()==""):
            b = 1.0
        else:
            b = float(self.e3.get())


        if (self.Proj.get()=="None"):
            proj = None
        else:
            proj = self.Proj.get()
            
        for cell in ["cell_"+str(i) for i in range(int(self.e1.get()),a+1)]:
            DR.FullEval(self.Dir+"/"+cell+"/",self.Mode.get(),bool(self.MC.get()),b,proj,self) #FullEval(Dir,Mode,Channels,Unit=1,z_type='SUM',frame=None)

        #except:
        #    alert_popup("Warning","Oops - something went wrong")

"""========================================================================================"""
class DataAnalyzeWindow(Frame):
    def __init__(self,master,Dir,Acceptable,tdict):
        self.input_num = 0 
        self.master = master
        self.Dir    =  Dir
        self.frame = Frame(self.master)
        self.master.title("Analysis Tool")
        #l2 = Label(self.master, text = "This is toplevel window")
        #l2.pack()
        self.master.configure(bg= "#99CBBB")
        self.master.geometry("400x400")

        self.l2= Label(self.master, text = "Enter Number of Datasets",bg="#DCE4EF", width=20, height=1)
        self.l2.grid(row=0, column=0, padx=20, pady=20)

       # self.l2_1= Label(self.master, text = "[Enter 1 for a single experiment analysis or >1 for cross experiment analysis]",bg="#DCE4EF", width=40, height=5)
       # self.l2_1.grid(row=1, column=0, padx=20, pady=20)
        self.Enter_box= Entry(self.master)
        self.Enter_box.grid(row=0, column=2, padx= 20, pady=20)
        enter_box_tip= CreateToolTip(self.Enter_box, 'Enter 1 for a single experiment analysis or >1 for cross experiment analysis' )

        enter_button= Button(self.master, text = "Enter", command= self.verify)
        enter_button.grid(row=0, column=3, padx=10, pady=10)



        self.my_button= {}
        self.my_entry= {}

        #if (isinstance( int(self.Enter_box.get()), int)):
            #self.input_num= int(self.Enter_box.get())
         # self.l1 = Label(self.master, text = self.folder_path,bg="#DCE4EF", width=20, height=1)

    def verify(self):
        try:
            int(self.Enter_box.get())
            self.input_num= int(self.Enter_box.get())
            self.dir_list= []
            for x in range(self.input_num):
          
                self.my_entry[x]= Entry(self.master)
                self.my_entry[x].grid(row=x+1, column= 2, padx=20, pady=20)
                self.my_button[x]= Button(self.master, text = "Choose Directory", command=lambda:self.dir_button(x, self.dir_list))
                self.my_button[x].grid(row=x+1, column= 3, padx=10) 
            
            self.graph_button= Button(self.master, text="Move to Analysis", command= self.move_to_anal)
            self.graph_button.grid(row=self.input_num+1, column= 2, padx=10, pady=20)
            
        except ValueError:
            messagebox.showerror('Enter an integer value!')


    # def move_to_anal(self):
    #     """Function to choose analysis type"""

    #     self.plt_window = Toplevel(self.master)
    #     my_notebook = ttk.Notebook(self.plt_window)
    #     my_notebook.grid(pady=15)

    #     spatial_frame= Frame(my_notebook, width=1000, height= 700)
    #     temporal_frame= Frame(my_notebook, width=1000, height= 700)
    #     custom_frame= Frame(my_notebook, width=1000, height= 700)


    #     spatial_frame.grid(row=0, column=0)
    #     temporal_frame.grid(row=0, column=0)
    #     custom_frame.grid(row=0, column=0)

    #     sub_frame_1= Frame(spatial_frame, width=200, height=700)
    #     sub_frame_1.grid(row=0, column=0)

    #     sub_frame_2= Frame(temporal_frame, width=200, height=700)
    #     sub_frame_2.grid(row=0, column=0)

    #     # sub_frame_3= Frame(custom_frame, width=200, height=1000)
    #     # sub_frame_3.grid(row=0, column=0)


    #     my_notebook.add(spatial_frame, text="Spatial Analysis")
    #     my_notebook.add(temporal_frame,text= "Temporal Analysis")
    #     my_notebook.add(custom_frame,text= "Custom Analysis")

    

   












        # self.spatial= Button(self.master, text="Spatial Analysis", command= lambda: self.spatial_analysis) #command= self.spatial_analysis)
        # self.spatial.grid(row=4, column= 2, padx=10, pady=10)
        # self.temporal= Button(self.master, text="Temporal Analysis", command= lambda: self.temporal_analysis) #command= self.spatial_analysis)
        # self.temporal.grid(row=5, column= 2, padx=10, pady=10)
        # self.custom= Button(self.master, text="Custom Plot", command= lambda: self.custom_plot) #command= self.spatial_analysis)
        # self.custom.grid(row=6, column= 2, padx=10, pady=10)




       
    def dir_button(self, x, dir_list):
        """Function that sets the desired folder and creates an array for all the directories"""
        
        filename = filedialog.askdirectory()
        Dir =str(filename)
        self.dir_list.append(Dir)

    def spatial_analysis(self):
        """Function to make spatial plots """

    def custom_plot(self):
        """Function to make custom plots"""

        #self.l4= Label(self.master, text = "",bg="#DCE4EF", width=20, height=1)

        options_1 = [
        "Line Chart",
        "Scatter",
        "Histogram",
    
        ]

        clicked = StringVar()
  

        clicked.set( "Choose Type of Graph" )
  

        drop_1 = OptionMenu( self.master, clicked , *options_1 )
        drop_1.grid(row=4, column=2, padx=10, pady=10)

        options_2 = [
        "Line Chart",
        "Scatter",
        "Histogram",
    
        ]

        clicked = StringVar()
  

        clicked.set( "Choose X-Axis" )
  

        drop_1 = OptionMenu( self.master, clicked , *options_2 )
        drop_1.grid(row=5, column=2, padx=10, pady=10)

        options_3 = [
        "Line Chart",
        "Scatter",
        "Histogram",
    
        ]

        clicked = StringVar()
  

        clicked.set( "Choose Y-Axis" )
  

        drop_1 = OptionMenu( self.master, clicked , *options_3 )
        drop_1.grid(row=6, column=2, padx=10, pady=10)










        



# class DataAnalyzeWindow(Frame):

#     """Class that defines the analyze data window"""
#     def __init__(self,master,Dir,Acceptable,tdict):

#         self.master = master
#         self.Dir    =  Dir
#         self.frame = Frame(self.master)

#         self.var = dict()
#         self.varbool = dict()
#         self.allvar = IntVar()
#         choices = { 'Dynamic line','Contour plot','Buckets'}

#         self.tkvar = StringVar(master)
#         self.tkvar.set('Dynamic line')
#         count=1

#         chk = Checkbutton(master, text='All', variable=self.allvar,command=lambda:self.reset())
#         chk.grid(row=0,column=0,padx=5, pady=5)

#         for cell in Acceptable:

#             self.var[cell[:-1]]=IntVar()
#             if(tdict[cell[:-1]]==2):
#                 chk_color = "red"
#             elif(tdict[cell[:-1]]==1):
#                 chk_color = "orange"
#             elif(tdict[cell[:-1]]==0):
#                 chk_color = "black"

#             chk = Checkbutton(master, text=cell[:-1], variable=self.var[cell[:-1]],fg=chk_color,
#                               command=lambda key=cell[:-1]: self.Readstatus(key))
#             chk.grid(row=count,column=0,padx=5, pady=5)

#             count += 1

#             self.varbool[cell[:-1]]=False

#         self.b1 = Button(master,text="Go!",command = self.IntPlotWindow)
#         self.b1.grid(row=int(count/2)+1,column=1,padx=5, pady=5)

#         self.popupMenu = OptionMenu(master, self.tkvar, *choices)
#         self.popupMenu.grid(row = int(count/2), column =1)
       
#         self.e1 = Entry(master,width=5)
#         self.e1.grid(row = int(count/2)-1, column =1)

    def IntPlotWindow(self):
        """Function that,based on the selection, runs the right analysis window"""

        Data,lenTime = DA.GetData(self.Dir,self.varbool)

        if(self.tkvar.get()=='Dynamic line'):
            DA.DataAnalWindow(Data,self.Dir,self.varbool,lenTime)

        elif(self.tkvar.get()=='Contour plot'):
            if(self.e1.get() == ''):
                DA.ContourWindow(Data,self.Dir,self.varbool,lenTime)
            else:
                contNum = [int(x) for x in self.e1.get().split(',')][0]
                DA.ContourWindow(Data,self.Dir,self.varbool,lenTime,contNum)

        elif(self.tkvar.get()=='Buckets'):
            Thresh = [float(x) for x in self.e1.get().split(',')]
            DA.MultiLineWindow(Data,self.Dir,Thresh,self.varbool,lenTime)

    def Readstatus(self,key):
        """Sets checkbuttons to the correct value"""

        var_obj = self.var.get(key)
        self.varbool[key] = bool(var_obj.get())

    def reset(self):
        """Resets buttons if All is clicked"""

        if self.allvar.get():

            for cell in self.var:
                var_obj = self.var.get(cell)
                var_obj.set(1)
                self.varbool[cell] = bool(var_obj.get())

        else:

            for cell in self.var:
                var_obj = self.var.get(cell)
                var_obj.set(0)
                self.varbool[cell] = bool(var_obj.get())

"""========================================================================================"""

class DeleteWindow(Frame):
    """Class that defines the clean data window"""
    def __init__(self,master,Dir):

        self.master = master
        self.frame = Frame(self.master)

        self.Dir   = Dir
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()

        c1 = Checkbutton(master, text="Shifting Direction", variable=self.var1)
        c1.grid(row=2,column=0,padx=5, pady=5)

        c2 = Checkbutton(master, text="Dendrite Files", variable=self.var2)
        c2.grid(row=3,column=0,padx=5, pady=5)

        c3 = Checkbutton(master, text="Json Files", variable=self.var3)
        c3.grid(row=4,column=0,padx=5, pady=5)

        c4 = Checkbutton(master, text="Roi picture", variable=self.var4)
        c4.grid(row=5,column=0,padx=5, pady=5)


        Label(master, text="Minimum Cell").grid(row = 0, column = 0)
        Label(master, text="Maximum Cell").grid(row = 1, column = 0)

        self.e1 = Entry(master)
        self.e1.grid(row=0,column=1,padx=5, pady=5)

        self.e2 = Entry(master)
        self.e2.grid(row=1,column=1,padx=5, pady=5)

        self.b1 = Button(master,text="Clean",command = self.clean_button)
        self.b1.grid(row=3,column=1,padx=5, pady=5)

    def clean_button(self):
        # Based on the selection the window will delete the chosen files - giving a warning
        # if they dont exist

        #try:
        temp = os.path.split(self.Dir)[-1]

        if(self.e2.get()==""):
            a = int(self.e1.get())

        else:
            a = int(self.e2.get())

        for cell in ["cell_"+str(i) for i in range(int(self.e1.get()),a+1)]:
            for x in os.listdir(self.Dir+"/"+cell+"/"):
                if("MinDir" in x and self.var1.get()==1):
                    self.delfile(self.Dir+"/"+cell+"/"+x)
                elif(("Dendrite" in x or "background" in x) and self.var2.get()==1):
                    self.delfile(self.Dir+"/"+cell+"/"+x)
                elif(".json" in x and self.var3.get()==1):
                    self.delfile(self.Dir+"/"+cell+"/"+x)
                elif("ROIs.png" in x and self.var1.get()==1):
                    self.delfile(self.Dir+"/"+cell+"/"+x)
        #except:
        #    alert_popup("Warning","Oops - something went wrong")

    def delfile(self,path):
        """Function that does the deleting"""

        if os.path.exists(path):
            os.remove(path)

        else:
            alert_popup("Warning","The file: " + path + " doesn't exist",w=500,h=100)

    def close_windows(self):
        self.master.destroy()

"""========================================================================================"""

def alert_popup(title, message,w=None,h=None):
    """Generate a pop-up window for special messages."""
    root = Toplevel()
    root.title(title)
    m = message
    m += '\n'
    w = Label(root, text=m)
    w.grid(row=0,column=0,padx=5, pady=5)
    b1 = Button(root, text="OK", command=root.destroy, width=10)
    b1.grid(row=1,column=0,padx=5, pady=5)





# def main_screen():
#     global img
#     global label
#     splash= Tk()
    

#     img = ImageTk.PhotoImage(Image.open("splash.png"))

#     label = Label(image=img)
#     label.grid(row=0, column=0, columnspan=3)

#     splash.after(3000)

#     splash.destroy()

if __name__ == '__main__':
    
    # splash= Tk()
    # splash.geometry= ("700x500")
    
    # frame = Frame(splash, width=600, height=400)
    # frame.pack()



    # img = ImageTk.PhotoImage(Image.open("splash.png"))

     

    # label = Label(frame, image=img)
    # label.pack()

    # splash.after(3000)

    # splash.destroy()

   
   Mw = MainScreen()
