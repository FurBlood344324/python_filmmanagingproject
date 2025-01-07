from pathlib import Path
import tkinter as tk
import sys, json, requests
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import simpledialog
from io import BytesIO
from tkinter.messagebox import askyesno

filtered = []
inputfilm = {}
selected_film = {}
LoginedUser = []
tmdbmovies = []
isAdd = False
isFilter = False
isEdit = False
apikey = ""

class Controller:
    def __init__(self):
        self.films = self.loadFilms()
        self.users = self.loadUsers()

    def loadFilms(self, userName=None):
        try:
            with open("films.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return []

        if userName:
            for user in data:
                if userName in user.keys():
                    return user[userName]
            return []
        else:
            return data

    def saveFilms(self, userName, filmsdata):
        index=-1
        isEqual=False
        try:
            with open("films.json", 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        for user in data:
            if userName in user.keys():
                index=data.index(user)
                isEqual=True
                user[userName] = filmsdata
                break
        if isEqual:
            data[index][userName] = filmsdata
        else:
            data.append({userName: filmsdata})   
            

        with open("films.json", 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def loadUsers(self):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def saveUsers(self, users):
        with open("users.json", "w") as f:
            json.dump(users, f)
    

class InitialApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for f in [FilmManegementFrame, FilmEntryFrame, FilmListFrame, LoginFrame, RegisterFrame, TMDBSearchFrame]:
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginFrame)

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
        
        self.image1 = Image.open(self.relative_to_assets("image_2.jpg"))
        self.photo1 = ImageTk.PhotoImage(self.image1)
        self.label_b = tk.Label(self, image=self.photo1)
        self.label_b.place(x=0, y=0)

        self.image2 = Image.open(self.relative_to_assets("image_3o.png")).resize((881,120))
        self.photo2 = ImageTk.PhotoImage(self.image2)

        self.label_t = tk.Label(
            self,
            compound="center",
            text="Film Management App",
            fg="#E5E4E2", 
            font=("coral", 36, "bold"),
            bg = "#2E3440",
            image=self.photo2
        )
        self.label_t.place(x=0, y=0)

        self.label_t1 = tk.Label(
            self,
            text="© 2024 Film Management App",
            fg="#F3F3F3",
            bg="#2E3440",  # Accent color
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

        self.TMDB_button = ttk.Button(
            self,
            text="TMDB Search",
            command=self.on_TMDB_button_clicked
        )
        self.TMDB_button.place(
            x=315.0,
            y=179.0,
            width=250.0,
            height=50.0
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
        self.infoButton = ttk.Button(
            self,
            text="Info",
            command= self.infoAboutApp
        )
        self.infoButton.place(
            x=315.0,
            y=356.0,
            width=250.0,
            height=50.0
        )
        
        self.exit_button = ttk.Button(
            self,
            text="Log Out",
            command=self.on_exit_button_clicked)
        
        self.exit_button.place( 
            x=315.0,
            y=415.0,
            width=250.0,
            height=50.0
        )
    def on_exit_button_clicked(self):
        self.controller1.show_frame(LoginFrame)

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
    def infoAboutApp(self):
        global infoPop
        self.infoPop = tk.Toplevel() 
        self.infoPop.title("Info about the app")
        self.infoPop.geometry("600x350")
        self.infoPop.configure(bg="#2E3440")
        self.headerLabel = tk.Label(self.infoPop, text="How to use", bg="#2E3440", fg="#FFBF00", font=("Helvetica", 30, "bold"))
        self.infoLabel = tk.Label(self.infoPop, 
                            text="""1. Click on Start button to add a film
2. Click on List button to view all films
3. Click on Filter button to filter films
4. Click on Edit button to edit a film
5. Click on Delete button to delete a film
6. Click on Back button to go back to previous screen""", 
                            bg="#2E3440", 
                            fg="#40E0D0", 
                            font=("Helvetica", 14, "bold"),
                            justify="left",
                            anchor="w",
                            padx=10
                            )
        self.headerLabel.place(x=200, y=10)
        self.infoLabel.place(x=10, y=75)
        self.gotItButton = tk.Button(self.infoPop, text="Got it!", command=self.infoPop.destroy, bg="#FFBF00", fg="#36454F",width=6, height=1,font=("Helvetica", 14, "bold"))
        self.gotItButton.place(x=400, y=250)
        self.infoPop.mainloop()

    def on_TMDB_button_clicked(self):
        self.controller1.show_frame(TMDBSearchFrame)

        

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

        label1 = tk.Label(
            self,
            text="Name",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        label1.place(
            x=152.5,
            y=75.0,
            width=100.0,
            height=37.0)
        self.name = tk.Entry(self)
        self.name.place(
            x=299.5,
            y=75.0,
            width=300.0,
            height=37.0
        )

        label2 = tk.Label(
            self,
            text="Type",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440", fg="#D8A657"
        )
        label2.place(
            x=152.5,
            y=150.0,
            width=100.0,
            height=37.0)
        self.type = ttk.Combobox(
            self,
            values=["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Thriller", "Romance", "Fantasy", "Animation", "Documentary"]
        )
        self.type.place(
            x=299.5,
            y=150.0,
            width=300.0,
            height=37.0
        )

        label3 = tk.Label(
            self,
            text="Status",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        label3.place(
            x=152.5,
            y=225.0,
            width=100.0,
            height=37.0)
        self.status = ttk.Combobox(
            self,
            values=["Watched", "Neglected"]
        )
        self.status.place(
            x=299.5,
            y=225.0,
            width=300.0,
            height=37.0
        )

        label4 = tk.Label(
            self,
            text="Star",
            font=("Helvetica", 14, "bold"), bg="#2E3440", fg="#D8A657")
        label4.place(
            x=152.5,
            y=300.0,
            width=100.0,
            height=37.0
        )
        self.star = StarRating(self)

        self.star.place(
            x=299.5,
            y=300.0,
            width=300.0,
            height=37.0
        )

        label5 = tk.Label(
            self,
            text="Note",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        label5.place(
            x=152.5,
            y=375.0,
            width=100.0,
            height=37.0
        )
        self.note = tk.Entry(self)
        self.note.place(
            x=299.5,
            y=375.0,
            width=300.0,
            height=37.0
        )

        button = tk.Button(
            self,
            text="Submit",
            command=lambda: self.on_submit_button_clicked(FilmListFrame, self.name, self.type, self.status, self.note),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        button.place(
            x=275.0,
            y=450.0,
            width=300.0,
            height=37.0
        )

        backbutton = tk.Button(
            self,
            text="Back",
            command=lambda: self.controller1.show_frame(FilmManegementFrame),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        backbutton.place(
            x=275.0,
            y=500.0,
            width=300.0,
            height=37.0
        )
    

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame1'
        return Path(__file__).parent / 'assets' / 'frame1'

    def on_submit_button_clicked(self, frame, name=None, type=None, status=None, note=None):
        global filtered, selected_film, inputfilm, isFilter, isEdit, isAdd, LoginedUser 
        c = Controller() 
        films = c.loadFilms(LoginedUser[0])
        inputfilm = {
            "name": name.get(),
            "type": type.get(),
            "status": status.get(),
            "star": self.star.get(),
            "note": note.get()
        }
        filtered = []
        temp_filtered = []
        if isAdd:
            try:
                if not name.get() or not type.get() or not status.get() or not self.star.get() or not note.get():
                    raise Exception("All fields are required")
            except Exception as e:
                tk.messagebox.showerror("Error", e)
                return
            films.append(inputfilm)
        if isFilter:
            filtered_films = films
            if name.get():
                temp_filtered = []
                for film in filtered_films:
                    if name.get().lower() in film["name"].lower():
                        temp_filtered.append(film)
                filtered_films = temp_filtered
            if type.get():
                temp_filtered = []
                for film in filtered_films:
                    if type.get().lower() in film["type"].lower():
                        temp_filtered.append(film)
                filtered_films = temp_filtered
            if status.get():
                temp_filtered = []
                for film in filtered_films:
                    if status.get().lower() in film["status"].lower():
                        temp_filtered.append(film)
                filtered_films = temp_filtered
            starRate = self.star.get()
            if starRate > 0:
                temp_filtered = []
                for film in filtered_films:
                    if film["star"] == starRate:
                        temp_filtered.append(film)
                filtered_films = temp_filtered
            if note.get():
                temp_filtered = []
                for film in filtered_films:
                    if note.get().lower() in film["note"].lower():
                        temp_filtered.append(film)
                filtered_films = temp_filtered
            filtered = filtered_films
        elif isEdit:
            answer = askyesno("Edit", "Are you sure you want to edit this film?")
            if not answer:
                return
            for i, film in enumerate(films):
                if film == selected_film:
                    films[i] = inputfilm
                    break
            c.saveFilms(LoginedUser[0], films)
            isEdit = False
        name.delete(0, tk.END)
        type.delete(0, tk.END)
        status.delete(0, tk.END)
        self.star.set_rating(0)
        note.delete(0, tk.END)
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

        self.image1 = Image.open(self.relative_to_assets("image_3o.png")).resize((400, 100))
        self.photo1 = ImageTk.PhotoImage(self.image1)

        self.label_t = tk.Label(
            self,
            compound="center",
            text="List of Films",
            fg="#F4BB44",
            font=("Inter", 40),
            image=self.photo1
        )
        self.label_t.place(x=250, y=20.0)

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#12A4D9", foreground="#2E3440", fieldbackground="#FF6E40")

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
            command=self.on_filter_button_clicked
        )
        self.filter_button.place(
            x=78.0,
            y=500.0,
            width=166.25,
            height=48.0
        )

        self.edit_button = ttk.Button(
            self,
            text="Edit",
            command=lambda: self.edit_data()
        )
        self.edit_button.place(
            x=264.25,
            y=500.0,
            width=166.25,
            height=48.0
        )

        self.delete_button = ttk.Button(
            self,
            text="Delete",
            command=lambda: self.delete_data()
        )
        self.delete_button.place(
            x=450.5,
            y=500.0,
            width=166.25,
            height=48.0
        )

        self.back_button = ttk.Button(
            self,
            text="Back",
            command=lambda: self.controller1.show_frame(FilmManegementFrame)
        )
        self.back_button.place(
            x=636.75,
            y=500.0,
            width=166.25,
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
        global inputfilm, LoginedUser
        c = Controller()
        films = c.loadFilms(LoginedUser[0])
        films.append(inputfilm)
        c.saveFilms(LoginedUser[0], films)
        self.list_data()

    def list_data(self):
        global LoginedUser
        c = Controller()
        films = c.loadFilms(LoginedUser[0])
        for i in self.tree.get_children():
            self.tree.delete(i)
        for film in films:
            if isinstance(film, dict):  # Ensure film is a dictionary
                self.tree.insert("", "end", values=(film.get("name"), film.get("type"), film.get("status"), film.get("star"), film.get("note")))

    def refresh_data(self):
        global filtered
        for i in self.tree.get_children():
            self.tree.delete(i)
        for film in filtered:
            self.tree.insert("", "end", values=(film["name"], film["type"], film["status"], film["star"], film["note"]))

    def edit_data(self):
        global isEdit, selected_film
        isEdit = True
        selected_item = self.tree.selection()
        try:
            if not selected_item:
                raise Exception("Please select a film to edit")
            if selected_item:
                film_values = self.tree.item(selected_item, "values")
                selected_film = {
                    "name": film_values[0],
                    "type": film_values[1],
                    "status": film_values[2],
                    "star": int(film_values[3]),
                    "note": film_values[4],
                }
            self.controller1.show_frame(FilmEntryFrame)
            fef = self.controller1.frames[FilmEntryFrame]
            fef.name.insert(0, selected_film["name"])
            fef.type.set(selected_film["type"])
            fef.status.set(selected_film["status"])
            fef.star.set_rating(selected_film["star"])
            fef.note.insert(0, selected_film["note"])
        except Exception as e:
            tk.messagebox.showerror("Error", e)
            return

    def delete_data(self):
        global LoginedUser
        c = Controller()
        films = c.loadFilms(LoginedUser[0])
        selected_item = self.tree.selection()
        try:
            if not selected_item:
                raise Exception("Please select a film to delete")
            if selected_item:
                film_values = self.tree.item(selected_item, "values")
                film_to_delete = {
                    "name": film_values[0],
                    "type": film_values[1],
                    "status": film_values[2],
                    "star": int(film_values[3]),
                    "note": film_values[4],
                }
            answer = askyesno("Delete", "Are you sure you want to delete this film?")
            if not answer:
                return
            for i, film in enumerate(films):
                if film == film_to_delete:
                    del films[i]
                    break
            self.tree.delete(selected_item)
            c.saveFilms(LoginedUser[0], films)
        except Exception as e:
            tk.messagebox.showerror("Error", e)
            return
class StarRating(tk.Frame):
    def __init__(self, parent, initial_rating=0):
        super().__init__(parent, bg="#2E3440")
        self.rating = tk.IntVar(value=initial_rating)
        self.stars = []
        
    
        self.clear_button = tk.Label(
            self,
            text="❌",
            font=("Arial", 20),
            bg="#2E3440",
            fg="#D70040",
            cursor="hand2"
        )
        self.clear_button.grid(row=0, column=5, padx=(10,2))
        self.clear_button.bind('<Button-1>', lambda e: self.set_rating(0))
        
        for i in range(5):
            star = tk.Label(
                self,
                text="★",
                font=("Arial", 20),
                bg="#2E3440",
                fg="#FFFFFF",
                cursor="hand2"
            )
            star.grid(row=0, column=i, padx=2)
            star.bind('<Button-1>', lambda e, index=i: self.set_rating(index + 1))
            star.bind('<Enter>', lambda e, index=i: self.hover(index + 1))
            star.bind('<Leave>', lambda e: self.leave())
            self.stars.append(star)
        
        if initial_rating > 0:
            self.set_rating(initial_rating)

    def set_rating(self, value):
        self.rating.set(value)
        self.update_stars()
    
    def get(self):
        return self.rating.get()
    
    def hover(self, value):
        for i in range(5):
            if i < value:
                self.stars[i].config(fg="#FFD700")
            else:
                self.stars[i].config(fg="#FFFFFF")
    
    def leave(self):
        self.update_stars()
    
    def update_stars(self):
        rating = self.rating.get()
        for i in range(5):
            if i < rating:
                self.stars[i].config(fg="#FFD700")
            else:
                self.stars[i].config(fg="#FFFFFF")

class LoginFrame(tk.Frame):
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
        
        self.image = Image.open(self.relative_to_assets("LoginBackground (2).jpg"))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_b = tk.Label(self, image=self.photo)
        self.label_b.place(x=0, y=0)

        labelUsername = tk.Label(
            self,
            text="Username",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        labelUsername.place(
            x=250,
            y=250.0,
            width=100.0,
            height=37.0
        )
        entryUsername = tk.Entry(self)
        entryUsername.place(
            x=400,
            y=250.0,
            width=200.0,
            height=37.0
        )
        labelPassword = tk.Label(
            self,
            text="Password",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        labelPassword.place(
            x=250,
            y=300.0,
            width=100.0,
            height=37.0
        )
        entryPassword = tk.Entry(self, show="*")
        entryPassword.place(
            x=400,
            y=300.0,
            width=200.0,
            height=37.0
        )
        submitButton = tk.Button(
            self,
            text="Submit",
            command=lambda: self.on_submit_button_clicked(entryUsername, entryPassword),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        submitButton.place(
            x=400,
            y=350.0,
            width=200.0,
            height=37.0
        )

        labelRegister = tk.Label(
            self,
            text="Don't have an account?",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        labelRegister.place(
            x=375,
            y=550.0,
            width=300.0,
            height=37.0
        )
        RegisterButton = tk.Button(
            self,
            text="Register",
            command=lambda: self.on_register_button_clicked(RegisterFrame),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        RegisterButton.place(
            x=700,
            y=550.0,
            width=150.0,
            height=37.0
        )

    def on_submit_button_clicked(self, entryUsername, entryPassword):
        global LoginedUser
        LoginedUser = []
        if not entryUsername.get() or not entryPassword.get():
            tk.messagebox.showerror("Error", "All fields are required")
            return
        c = Controller()
        users = c.loadUsers()
        for user in users:
            if user["username"] == entryUsername.get() and user["password"] == entryPassword.get():
                LoginedUser.append(entryUsername.get())
                LoginedUser.append(entryPassword.get())
                entryUsername.delete(0, tk.END)
                entryPassword.delete(0, tk.END)
                self.controller1.show_frame(FilmManegementFrame)
                return
        tk.messagebox.showerror("Error", "Invalid username or password")
    
    def on_register_button_clicked(self,frame):
        self.controller1.show_frame(RegisterFrame)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame3'
        return Path(__file__).parent / 'assets' / 'frame3'

class RegisterFrame(tk.Frame):
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
        
        self.image = Image.open(self.relative_to_assets("LoginBackground (2).jpg"))
        self.photo = ImageTk.PhotoImage(self.image)
        self.label_b = tk.Label(self, image=self.photo)
        self.label_b.place(x=0, y=0)
    
        labelUsername = tk.Label(
            self,
            text="Username",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        labelUsername.place(
            x=250,
            y=250.0,
            width=100.0,
            height=37.0
        )

        entryUsername = tk.Entry(self)
        entryUsername.place(
            x=400,
            y=250.0,
            width=200.0,
            height=37.0
        )

        labelPassword = tk.Label(
            self,
            text="Password",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        labelPassword.place(
            x=250,
            y=300.0,
            width=100.0,
            height=37.0
        )
        entryPassword = tk.Entry(self, show="*")
        entryPassword.place(
            x=400,
            y=300.0,
            width=200.0,
            height=37.0
        )

        submitButton = tk.Button(
            self,
            text="Submit",
            command=lambda: self.on_submit_button_clicked(entryUsername, entryPassword),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        submitButton.place(
            x=400,
            y=350.0,
            width=200.0,
            height=37.0
        )

        BackButton = tk.Button(
            self,
            text="Back",
            command=lambda: self.on_back_button_clicked(LoginFrame),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        BackButton.place(
            x=400, 
            y=400.0,
            width=200.0,
            height=37.0
        )

    def on_submit_button_clicked(self, entryUsername, entryPassword):
        username = entryUsername.get()
        password = entryPassword.get()
        if not username or not password:
            tk.messagebox.showerror("Error", "All fields are required")
            return
        else:
            c = Controller()
            users = c.loadUsers()
            for user in users:
                if user["username"] == username:
                    tk.messagebox.showerror("Error", "Username already exists")
                    return
            users.append({"username": username, "password": password})
            c.saveUsers(users)
            tk.messagebox.showinfo("Success", "You have successfully registered")
            entryUsername.delete(0, tk.END)
            entryPassword.delete(0, tk.END)
            self.controller1.show_frame(LoginFrame) 

    def on_back_button_clicked(self, frame):
        self.controller1.show_frame(LoginFrame)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame4'
        return Path(__file__).parent / 'assets' / 'frame4'


class TMDBSearchFrame(tk.Frame):
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
    
        labelSearch = tk.Label(
            self,
            text="Search",
            font=("Helvetica", 14, "bold"),
            bg="#2E3440",
            fg="#D8A657"
        )
        labelSearch.place(
            x=250,
            y=250.0,
            width=100.0,
            height=37.0
        )

        entrySearch = tk.Entry(self)
        entrySearch.place(
            x=400,
            y=250.0,
            width=200.0,
            height=37.0
        )

        submitButton = tk.Button(
            self,
            text="Submit",
            command=lambda: self.on_submit_button_clicked(entrySearch),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        submitButton.place(
            x=400,
            y=300.0,
            width=200.0,
            height=37.0
        )

        BackButton = tk.Button(
            self,
            text="Back",
            command=lambda: self.on_back_button_clicked(FilmManegementFrame),
            bg="#D8A657",
            fg="#2E3440",
            font=("Helvetica", 14, "bold")
        )
        BackButton.place(
            x=400, 
            y=350.0,
            width=200.0,
            height=37.0
        )

    def on_submit_button_clicked(self, entrySearch):
        global apikey, tmdbmovies
        url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": apikey,
            "query": entrySearch.get(),
            "language": "tr-TR",
            "page": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])
        tmdbmovies = []

        for i, movie in enumerate(results[:1]):  # İlk 3 sonucu göster
            title = movie.get("title", "Bilinmiyor")
            release_date = movie.get("release_date", "Bilinmiyor")
            banner = movie.get("poster_path", "")
            description = movie.get("overview", "")
            self.add_movie_to_db(title, banner, release_date, description)

        global tmdbPop
        self.tmdbPop = tk.Toplevel() 
        self.tmdbPop.title("Info about the app")
        self.tmdbPop.geometry("500x500")
        self.tmdbPop.configure(bg="#2E3440")
        self.headerLabel = tk.Label(self.tmdbPop, text="TMDB Search", bg="#2E3440", fg="#FFBF00", font=("Helvetica", 30, "bold"))
        self.titlelabel = tk.Label(self.tmdbPop, text=f"Title: {tmdbmovies[0]['name']}", bg="#2E3440", fg="#FFBF00", font=("Helvetica", 14, "bold"))
        self.releaselabel = tk.Label(self.tmdbPop, text=f"Release Date: {tmdbmovies[0]['release_date']}", bg="#2E3440", fg="#FFBF00", font=("Helvetica", 14, "bold"))
        response1 = requests.get(tmdbmovies[0]['banner'])
        response1.raise_for_status()
        image_data = BytesIO(response1.content)
        image = Image.open(image_data)
        resized_image = image.resize((200, 250), Image.Resampling.LANCZOS)
        image_tk = ImageTk.PhotoImage(resized_image)
        self.banner = tk.Label(self.tmdbPop, image=image_tk) 
        self.banner.image = image_tk
        self.headerLabel.place(x=125, y=10)
        self.titlelabel.place(x=10, y=75)
        self.releaselabel.place(x=10, y=125)
        self.banner.place(x=10, y=175)
        print(tmdbmovies[0]['description'])


    def on_back_button_clicked(self, frame):
        self.controller1.show_frame(FilmManegementFrame)

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def get_base_path(self):
        if hasattr(sys, '_MEIPASS'):
            return Path(sys._MEIPASS) / 'assets' / 'frame5'
        return Path(__file__).parent / 'assets' / 'frame5'
    
    def add_movie_to_db(self, name, banner, release_date, description):
        global tmdbmovies
        status = "Neglected"
        base_url = "https://image.tmdb.org/t/p/w500"
        banner_url = f"{base_url}{banner}" if banner else ""
        tmdbmovies.append({
                "name": name,
                "status": status,
                "banner": banner_url,
                "release_date": release_date,
                "description": description
                })

app = InitialApp()
app.mainloop()
