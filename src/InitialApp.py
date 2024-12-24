from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button
import tkinter as tk
import sys
from tkinter import ttk
from PIL import Image, ImageTk

#Ana Sayfaya Dön butonu eklenecek

films = [
    {"name": "The Matrix","type": "Sci-Fi" ,"status" : "Watched","star": 5, "note" : "1"},
    {"name": "Inception","type": "Sci-Fi" ,"status" : "Not Watched", "star": 4, "note" : "2"},
    {"name": "The Dark Knight","type": "Action" ,"status" : "Watched", "star": 5, "note" : "3"},
    {"name": "The Matrix Reloaded","type": "Sci-Fi" , "status" : "Watched", "star": 4, "note" : "4"}
]

filtered = []
addedfilm = {}
selected_film = {}

isAdd = False
isFilter = False
isEdit = False


class InitialApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in [FilmManegementFrame, FilmEntryFrame, FilmListFrame]:
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FilmManegementFrame)

    def show_frame(self, cont):
        global isAdd, isFilter, isEdit
        frame = self.frames[cont]
        frame.tkraise()

        if cont == FilmListFrame and hasattr(frame, 'add_data') and isAdd:
            isAdd = False
            frame.add_data()
        elif cont == FilmListFrame and hasattr(frame, 'refresh_data') and isFilter:
            isFilter = False
            frame.refresh_data()
        elif cont == FilmListFrame and hasattr(frame, 'edit_data') and isEdit:
            isEdit = False
            frame.edit_data()
        elif cont == FilmListFrame and hasattr(frame, 'list_data'):
            frame.list_data()
        

class FilmManegementFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller1 = controller

        self.config(
            width=881, 
            height=599, 
            bg="#2E3440",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.ASSETS_PATH = self.get_base_path() 
        self.grid_propagate(False) 
        self.pack_propagate(False)
        
        self.image = Image.open(self.relative_to_assets("image_2.jpg"))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_b = tk.Label(self, image=self.photo)
        self.label_b.place(x=0, y=0)

        self.label_t = tk.Label(
            self,
            anchor="nw",
            text="Film Management App",
            fg="#FF7F50", 
            font=("coral", 62, "bold"),
            bg = "#2E3440"
        )
        self.label_t.place(x=0.0, y=0.0)

        self.label_t1 = tk.Label(
            self,
            text="© 2024 Film Management App",
            fg="#FF7F50",  # Accent color
            font=("Helvetica", 10)
        )
        self.label_t1.place(x=340.0, y=570.0)

        style = ttk.Style()
        style.theme_use("clam")  # Modern ttk theme
        style.configure(
            "TButton",
            font=("Helvetica", 14, "bold"),
            padding=8,
            background="#D8A657",  # Soft yellow tone
            foreground="#2E3440",  # Dark text for contrast
            borderwidth=2,
            relief="flat"
        )
        style.map(
            "TButton",
            background=[("active", "#A3BE8C")],  # Greenish tone on hover
            relief=[("pressed", "flat")]
        )

        self.start_button = ttk.Button(
            self,
            text="Start",
            command= self.on_start_button_clicked
        )
        self.start_button.place(
            x=315.0,
            y=238.0,
            width=250.0,
            height=50.0
        )

        self.list_button = ttk.Button(
            self,
            text="List",
            command= self.on_list_button_clicked
        )
        self.list_button.place(
            x=315.0,
            y=297.0,
            width=250.0,
            height=50.0
        )
        

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame0'
        return Path(__file__).parent / 'assets' / 'frame0' 
    
    def on_start_button_clicked(self):
        global isAdd
        isAdd = True
        self.controller1.show_frame(FilmEntryFrame)

    def on_list_button_clicked(self):
        global isAdd
        isAdd = False
        self.controller1.show_frame(FilmListFrame)

class FilmEntryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller1 = controller

        self.config(
            width=881, 
            height=599, 
            bg="#2E3440",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.ASSETS_PATH = self.get_base_path() 
        self.grid_propagate(False) 
        self.pack_propagate(False)

        self.image = Image.open(self.relative_to_assets("image_2.jpg"))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_b = tk.Label(self, image=self.photo)
        self.label_b.place(x=0, y=0)

        label1=tk.Label(
            self, 
            text="Name", 
            font=("Helvetica", 14, "bold"), 
            bg="#2E3440", 
            fg="#D8A657"
        )
        label1.place(x=78.0, y=75.0, width=100.0, height=37.0)
        self.name = tk.Entry(self)
        self.name.place(
            x=225.0, 
            y=75.0, 
            width=300.0, 
            height=37.0
        )

        label2=tk.Label(
            self, 
            text="Type", 
            font=("Helvetica", 14, "bold"), 
            bg="#2E3440", fg="#D8A657"
        )
        label2.place(x=78.0, y=150.0, width=100.0, height=37.0)
        self.type = ttk.Combobox(
            self,
            values=["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]
        )
        self.type.place(
            x=225.0, 
            y=150.0, 
            width=300.0, 
            height=37.0
        )

        label3=tk.Label(
            self, 
            text="Status", 
            font=("Helvetica", 14, "bold"), 
            bg="#2E3440", 
            fg="#D8A657"
        )
        label3.place(x=78.0, y=225.0, width=100.0, height=37.0)
        self.status = ttk.Combobox(
            self,
            values=["Watched", "Not Watched"]
        )
        self.status.place(
            x=225.0, 
            y=225.0, 
            width=300.0, 
            height=37.0
        )

        label4=tk.Label(
            self, 
            text="Star", 
            font=("Helvetica", 14, "bold"), bg="#2E3440", fg="#D8A657")
        label4.place(
            x=78.0, 
            y=300.0, 
            width=100.0, 
            height=37.0
        )
        self.star = tk.Spinbox(
            self,
            from_= 0,
            to = 5,
            wrap = True
        )
        self.star.place(
            x=225.0, 
            y=300.0, 
            width=300.0, 
            height=37.0
        )

        label5=tk.Label(
            self, 
            text="Note", 
            font=("Helvetica", 14, "bold"), 
            bg="#2E3440", 
            fg="#D8A657"
        )
        label5.place(
            x=78.0, 
            y=375.0, 
            width=100.0, 
            height=37.0
        )
        self.note = tk.Entry(self)
        self.note.place(
            x=225.0, 
            y=375.0, 
            width=300.0, 
            height=37.0
        )

        button = tk.Button(
            self, 
            text="Submit", 
            command=lambda : self.on_submit_button_clicked(FilmListFrame, self.name.get(), self.type.get(), self.status.get(), self.star.get(), self.note.get()),
            bg="#D8A657", 
            fg="#2E3440", 
            font=("Helvetica", 14, "bold")
        )
        button.place(
            x=225.0, 
            y=450.0, 
            width=300.0, 
            height=37.0
        )


    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame1'
        return Path(__file__).parent / 'assets' / 'frame1' 
    
    def on_submit_button_clicked(self, frame, name=None,type=None,status=None,star=None,note=None):
        global films
        global filtered
        global addedfilm
        addedfilm = {}
        addedfilm["name"] = name
        addedfilm["type"] = type
        addedfilm["status"] = status
        addedfilm["star"] = int(star)
        addedfilm["note"] = note
        filtered = []
        temp_filtered = []
        filtered_films = films
        if name:
            temp_filtered = []
            for film in filtered_films:
                if name.lower() in film["name"].lower():
                    temp_filtered.append(film)
            filtered_films = temp_filtered
        if type:
            temp_filtered = []
            for film in filtered_films:
                if type.lower() in film["type"].lower():
                    temp_filtered.append(film)
            filtered_films = temp_filtered

        if status:
            temp_filtered = []
            for film in filtered_films:
                if status.lower() in film["status"].lower():
                    temp_filtered.append(film)
            filtered_films = temp_filtered
        if star != "0":
            temp_filtered = []
            for film in filtered_films:
                if film["star"] == int(star):
                    temp_filtered.append(film)
            filtered_films = temp_filtered

        if note:
            temp_filtered = []
            for film in filtered_films:
                if note.lower() in film["note"].lower():
                    temp_filtered.append(film)
            filtered_films = temp_filtered
        filtered = filtered_films
        print(filtered)
        self.controller1.show_frame(frame)
        

class FilmListFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller1 = controller

        self.config(
            width=881, 
            height=599, 
            bg="#2E3440",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.ASSETS_PATH = self.get_base_path() 
        self.grid_propagate(False) 
        self.pack_propagate(False)

        self.image = Image.open(self.relative_to_assets("image_2.jpg"))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_b = tk.Label(self, image=self.photo)
        self.label_b.place(x=0, y=0)

        self.label_t = tk.Label(
            self,
            text="List of Films",
            fg="#000000",
            font=("Inter", 29 * -1)
        )
        self.label_t.place(x=361.0, y=47.0)

        self.tree = ttk.Treeview(
            self,
            columns=("Name", "Type", "Status", "Star", "Note"),
            show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Star", text="Star")
        self.tree.heading("Note", text="Note")
        self.tree.column('Name', width=200)
        self.tree.column('Type', width=125)
        self.tree.column('Status', width=125)
        self.tree.column('Star', width=75)
        self.tree.column('Note', width=200)
        self.tree.place(x=78.0, y=123.0, width=725.0, height=337.0)

        self.filter_button = ttk.Button(
            self,
            text="Filter",
            command= self.on_filter_button_clicked
        )
        self.filter_button.place(
            x=78.0,
            y=500.0,
            width=186.0,
            height=48.0
        )

        self.edit_button = ttk.Button(
            self,
            text="Edit",
            command= lambda: print("Edit button clicked")
        )
        self.edit_button.place(
            x=347.5,
            y=500.0,
            width=186.0,
            height=48.0
        )

        self.delete_button = ttk.Button(
            self,
            text="Delete",
            command= lambda: self.delete_data()
        )
        self.delete_button.place(
            x=617.0,
            y=500.0,
            width=186.0,
            height=48.0
        )


    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)
    
    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame2'
        return Path(__file__).parent / 'assets' / 'frame2'
    
    def on_filter_button_clicked(self):
        global isFilter
        isFilter = True
        self.controller1.show_frame(FilmEntryFrame)

    def add_data(self):
        global films
        global addedfilm
        films.append(addedfilm)
        self.list_data()

    
    def list_data(self):
        global films
        for i in self.tree.get_children():
            self.tree.delete(i)
        for film in films:
            self.tree.insert("", "end", values=(film["name"], film["type"], film["status"], film["star"], film["note"]))
    
    def refresh_data(self):
        print("Refreshing data")
        global filtered
        for i in self.tree.get_children():
            self.tree.delete(i)
        for film in filtered:
            self.tree.insert("", "end", values=(film["name"], film["type"], film["status"], film["star"], film["note"]))

    def edit_data(self):
        global isEdit
        isEdit = True
        self.controller1.show_frame(FilmEntryFrame)

    def delete_data(self):
        global films
        selected_item = self.tree.selection()  # Seçilen öğeyi al
        if selected_item:
        # Seçilen öğenin değerlerini al (tüm sütunlar)
            film_values = self.tree.item(selected_item, "values")
            film_to_delete = {
                "name": film_values[0],
                "type": film_values[1],
                "status": film_values[2],
                "star": int(film_values[3]),
                "note": film_values[4],
            }

        # Tüm bileşenlere göre eşleşen filmi bul ve sil
        for i, film in enumerate(films):
            if film == film_to_delete:
                del films[i]
                break

        self.tree.delete(selected_item)  # Treeview'den öğeyi sil
        print(f"{film_to_delete['name']} başariyla silindi.")
        print(films)
    
app = InitialApp()
app.mainloop()
