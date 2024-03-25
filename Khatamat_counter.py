import tkinter as tk
from ttkthemes import ThemedTk
import pandas as pd
import os
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, date

EXCEL_PATH = 'Khatamat_Counter.xlsx'
        
def open_or_create_excel(file_path):
    if not os.path.exists(file_path):
        # Create a new Excel file with specified columns
        columns = ['Khatma Name', 'Current Position', 'Total Khatmat', 'Todays Read','Last Read date','Last Khatma Date']
        df = pd.DataFrame(columns=columns)
        data = {
    'اسم السورة': ['الفاتحة', 'البقرة', 'آل عمران', 'النساء', 'المائدة', 'الأنعام', 'الأعراف', 'الأنفال', 'التوبة', 'يونس', 'هود', 'يوسف', 'الرعد', 'ابراهيم', 'الحجر', 'النحل', 'الإسراء', 'الكهف', 'مريم', 'طه', 'الأنبياء', 'الحج', 'المؤمنون', 'النور', 'الفرقان', 'الشعراء', 'النمل', 'القصص', 'العنكبوت', 'الروم', 'لقمان', 'السجدة', 'الأحزاب', 'سبأ', 'فاطر', 'يس', 'الصافات', 'سورة ص', 'الزمر', 'غافر', 'فصلت', 'الشورى', 'الزخرف', 'الدخان', 'الجاثية', 'الأحقاف', 'محمد', 'الفتح', 'الحجرات', 'سورة ق', 'الذاريات', 'الطور', 'النجم', 'القمر', 'الرحمن', 'الواقعة', 'الحديد', 'المجادلة', 'الحشر', 'الممتحنة', 'الصف', 'الجمعة', 'المنافقون', 'التغابن', 'الطلاق', 'التحريم', 'الملك', 'القلم', 'الحاقة', 'المعارج', 'نوح', 'الجن', 'المزمل', 'المدثر', 'القيامة', 'الإنسان', 'المرسلات', 'النبأ', 'النازعات', 'عبس', 'التكوير', 'الإنفطار', 'المطففين', 'الانشقاق', 'البروج', 'الطارق', 'الأعلى', 'الغاشية', 'الفجر', 'البلد', 'الشمس', 'الليل', 'الضحى', 'الشرح', 'التين', 'العلق', 'القدر', 'البينة', 'الزلزلة', 'العاديات', 'القارعة', 'التكاثر', 'العصر', 'الهمزة', 'الفيل', 'قريش', 'الماعون', 'الكوثر', 'الكافرون', 'النصر', 'المسد', 'الإخلاص', 'الفلق', 'الناس'],
    'الصفحة': [1, 2, 50, 77, 106, 128, 151, 177, 187, 208, 221, 235, 249, 255, 262, 267, 282, 293, 305, 312, 322, 332, 342, 350, 359, 367, 377, 385, 396, 404, 411, 415, 418, 428, 434, 440, 446, 453, 458, 467, 477, 483, 489, 496, 499, 502, 507, 511, 515, 518, 520, 523, 526, 528, 531, 534, 537, 542, 545, 549, 551, 553, 554, 556, 558, 560, 562, 564, 566, 568, 570, 572, 574, 575, 577, 578, 580, 582, 583, 585, 586, 587, 587, 589, 590, 591, 591, 592, 593, 594, 595, 595, 596, 596, 597, 597, 598, 598, 599, 599, 600, 600, 601, 601, 601, 602, 602, 602, 603, 603, 603, 604, 604, 604]
}
        df_sowar = pd.DataFrame(data)
        writer = pd.ExcelWriter(file_path, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Khatamat', index=False)
        df_sowar.to_excel(writer, sheet_name='SowarList', index=False)
        writer.close()
        
            
    return pd.read_excel(file_path, sheet_name='Khatamat'), pd.read_excel(file_path, sheet_name='SowarList')

class KhatamatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Khatamat App")   
        self.load_data()
        self.create_widgets()


    def load_data(self):
        self.data,self.SowarList = open_or_create_excel(EXCEL_PATH)
        if self.data['Last Read date'].empty:
            pass
        else:
            last_read_date = pd.Timestamp(self.data['Last Read date'][0]).day
            time_now = pd.Timestamp(datetime.now()).day
    
            # Subtracting the current day from the timestamp
            days_difference = (time_now-last_read_date)
            if days_difference > 0:
                self.data['Todays Read'] = 0
                self.data['Last Read date'] = datetime.now()
            
        

    def create_widgets(self):
        
        # Change background color of a button using the style object
        style = ttk.Style(root)
        style.configure("TFrame", background="#31363F")
        style.configure("TButton", background="#222831", font=("Arial", 12, "bold"),foreground="#76ABAE")
        style.configure("TLabel", background="#31363F", foreground="#76ABAE",font=("Arial", 10, "bold"))
        style.configure("TRadiobutton", background="#31363F", foreground="#EEEEEE",font=("Arial", 10, "bold"))
        
        # Label to display current Khatamat
        self.current_khatamat_label = ttk.Label(self.root, text="Current Khatamat : {}".format(self.data.shape[0]))
        self.current_khatamat_label.pack(pady=10)
        
        total_progress = self.calculate_total_progress()
        self.today_progress_label = ttk.Label(self.root, text=f"Today's Progress : {total_progress} pages")
        self.today_progress_label.pack(pady=10)

        # Frame to hold individual boxes
        self.box_frame = ttk.Frame(self.root)
        
        self.box_frame.pack()

        self.boxes = []  # List to hold box widgets

        for index, row in self.data.iterrows():
            box = KhatmaBox(self.box_frame, row, index,self.SowarList)
            box.pack(pady=10)
            self.boxes.append(box)

        # Button to update positions
        self.update_positions_button = ttk.Button(self.root, text="Update Positions", command=self.update_positions, width=30, cursor="hand2", takefocus=False)
        self.update_positions_button.pack(pady=10)
        
        # Button to add a new Khatma
        self.add_khatma_button = ttk.Button(self.root, text="Add New Khatma", command=self.add_new_khatma, width=30, cursor="hand2", takefocus=False)
        self.add_khatma_button.pack(pady=20)

    def updae_database(self):
         with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl') as writer:
            self.data.to_excel(writer, sheet_name='Khatamat', index=False)
            self.SowarList.to_excel(writer, sheet_name='SowarList', index=False)
            writer.save()
        
    def update_positions(self):
        for box in self.boxes:
            box.update_position(self.data)

        self.updae_database()
        
        self.current_khatamat_label.config(text="Current Khatamat : {}".format(self.data.shape[0]))
        
        total_progress = self.calculate_total_progress()
        self.today_progress_label.config(text=f"Today's Progress : {total_progress} pages")
        
        messagebox.showinfo("Success", "Positions updated successfully!")
        
    def add_new_khatma(self):
    # Create a popup window for the user to input the name
        name_popup = tk.Toplevel(self.root)
        name_popup.title("Enter New Khatma Name")

        # Label and entry for the name
        ttk.Label(name_popup, text="Enter the name for the new Khatma:").pack(pady=5)
        name_entry = ttk.Entry(name_popup)
        name_entry.pack(pady=5)
        curent_position = ttk.Entry(name_popup)
        curent_position.pack(pady=5)
        

        def add_khatma_with_name():
            # Get the name entered by the user
            new_khatma_name = name_entry.get()
            new_khatma_curent_position = curent_position.get()
            
            # Check if a name is entered
            if new_khatma_name:
                # Create the new Khatma DataFrame
                new_khatma = pd.DataFrame({
                    "Khatma Name": [new_khatma_name],
                    "Current Position": [int(new_khatma_curent_position)],
                    "Total Khatmat": [0],
                    "Todays Read": [0],
                    "Last Read date": [datetime.now()],
                    "Khatma Date": [None]  # Assuming 'Khatma Date' is a datetime column
                })
                self.data = pd.concat([self.data, new_khatma], ignore_index=True)

                # Create a new KhatmaBox widget for the new Khatma
                new_box = KhatmaBox(self.box_frame, new_khatma.iloc[0], len(self.data) - 1)
                new_box.pack(pady=10)
                self.boxes.append(new_box)

                # Update the current Khatamat label
                self.current_khatamat_label.config(text="Current Khatamat: {}".format(self.data.shape[0]))

                # Close the popup window
                self.updae_database()
                name_popup.destroy()
            else:
                # Show an error message if no name is entered
                messagebox.showerror("Error", "Please enter a name for the new Khatma.")

        # Button to add the new Khatma with the entered name
        ttk.Button(name_popup, text="Add Khatma", command=add_khatma_with_name).pack(pady=5)

        # Keep the popup window open until the user provides input
        name_popup.mainloop()
        
    def calculate_total_progress(self):
        total_progress = self.data['Todays Read'].sum()
        return total_progress
                        
class KhatmaBox(ttk.Frame):
    def __init__(self, parent, data, index,SowarList):
        super().__init__(parent)
        self.data = data
        self.data.name = index
        self.initial_position = data['Current Position']  # Store initial position
        self.SowarList = SowarList
        self.current_sora = '' 
        self.current_sora_index= 0
        self.current_sora_pages_number=0
        self.sora_progress=0
        
        # Label to display Khatma name and current position
        name_label_text = f"{self.data['Khatma Name']}"
        self.name_label = ttk.Label(self, text=name_label_text, width=20, anchor='center', font=("Arial", 12, "bold"))
        self.name_label.grid(row=3, column=0, padx=10, pady=5)

        # Label to display Current Position in the Khatma
        label_text_khatma = f"Current Position: {self.data['Current Position']}"
        self.label_khatma = ttk.Label(self, text=label_text_khatma, width=20)
        self.label_khatma.grid(row=0, column=1)
        self.progress_khatma = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate', value=data['Current Position'], maximum=604)
        self.progress_khatma.grid(row=1, column=1, padx=20,pady=5)
        
        # Label to display Current  Goz2 Position
        label_text_goz2 = f"Current Juzz': {int(self.data['Current Position']/20)}"
        self.label_goz2 = ttk.Label(self, text=label_text_goz2, width=20)
        self.label_goz2.grid(row=2, column=1)
        self.progress_goz2 = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate', value=data['Current Position']%20, maximum=20)
        self.progress_goz2.grid(row=3, column=1, padx=20,pady=5)
        
        # Label to display Current sora
        self.get_current_sora_info(self.initial_position)    
        label_text_sora = f"Current Sora : {self.current_sora} - ({self.sora_progress}/{self.current_sora_pages_number})"
        self.label_sora = ttk.Label(self, text=label_text_sora)
        self.label_sora.grid(row=4, column=1)
        self.progress_sora = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=200, mode='determinate', value=self.sora_progress, maximum=self.current_sora_pages_number)
        self.progress_sora.grid(row=5, column=1, padx=20,pady=5)

        # Radio buttons
        self.var = tk.IntVar()
        self.var.set(0)  # Initial state

        nochange = ttk.Radiobutton(self, text="Keep", variable=self.var, value=0)
        nochange.grid(row=6, column=0, padx=5)

        add_custom_button = ttk.Radiobutton(self, text="Add custom number", variable=self.var, value=1)
        add_custom_button.grid(row=6, column=1, padx=10)

        # Entry for custom number
        self.custom_entry = ttk.Entry(self)
        self.custom_entry.grid(row=6, column=2, padx=10)
        self.custom_entry.insert(0, "1")  # Set default value

        change_position_button = ttk.Radiobutton(self, text="Change to another position", variable=self.var, value=2)
        change_position_button.grid(row=6, column=3, padx=10)

        # Entry for custom position
        self.position_entry = ttk.Entry(self)
        self.position_entry.grid(row=6, column=4, padx=10)
        self.position_entry.insert(0, f"{data['Current Position']}")  # Set default value

        
        self.line = ttk.Separator(self, orient='horizontal')
        self.line.grid(row=7, column=0, columnspan=5, sticky="ew", pady=10)

    def update_position(self, data):
        selected_action = self.var.get()

        if selected_action == 1:
            try:
                custom_number = int(self.custom_entry.get())
                data.loc[self.data.name, 'Current Position'] += custom_number
                data.loc[self.data.name, 'Todays Read'] += custom_number
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
        elif selected_action == 2:
            try:
                Position = int(self.position_entry.get())
                data.loc[self.data.name, 'Current Position'] = Position
                added_reads = Position - self.initial_position
                if added_reads >= 0:
                    data.loc[self.data.name, 'Todays Read'] = added_reads
                else:
                    data.loc[self.data.name, 'Todays Read'] = 0
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")
        new_position = data.loc[self.data.name, 'Current Position']
        
        self.label_khatma.config(text=f"Current Position: {data.loc[self.data.name, 'Current Position']}")
        self.progress_khatma.config(value=data.loc[self.data.name, 'Current Position'])
        self.label_goz2.config(text=f"Current Juzz': {int(data.loc[self.data.name, 'Current Position']/20)}")
        self.progress_goz2.config(value=data.loc[self.data.name, 'Current Position']%20)
        self.get_current_sora_info(new_position)
        self.label_sora.config(text=f"Current Sora : {self.current_sora} - ({self.sora_progress}/{self.current_sora_pages_number})")
        self.progress_sora.config(value=self.sora_progress)
        return data
    def get_current_sora_info(self,position):
        if position == 0:
            position+=1
        self.current_sora = self.SowarList[self.SowarList['الصفحة'] <= position]['اسم السورة'].iloc[-1]
        self.current_sora_index = self.SowarList[self.SowarList['الصفحة'] <= position].index[-1] + 1
        next_sora_index = self.current_sora_index + 1
        current_sora_page = self.SowarList['الصفحة'].iloc[self.current_sora_index-1]
        next_sora_page = self.SowarList['الصفحة'].iloc[next_sora_index-1]
        self.current_sora_pages_number = next_sora_page - current_sora_page
        self.sora_progress = position - current_sora_page

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    root.configure(background="#31363F")
    app = KhatamatApp(root)
    root.mainloop()

#--------------------------------------------------------------
