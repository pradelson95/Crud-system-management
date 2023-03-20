from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3


main_window = Tk()
main_window.geometry("300x300")


def next_window():
    entry_username.get()
    entry_password.get()
    # validando los campos de username y password
    if entry_username.get() == "" and entry_password.get() == "":
        main_window.destroy()

        # crear la base de datos
        conn = sqlite3.connect('silvia_craft_store')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS texto (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    nombre TEXT,
                                    telefono TEXT,
                                    ciudad TEXT,
                                    direccion TEXT)''')
        conn.commit()

        root = Tk()
        root.geometry("1200x600")
        root.config(background="DarkOrchid4")

        top_frame = Frame(root, background="dark turquoise", width=1600, height=60)
        top_frame.place(x=0, y=0)

        label_top_frame = Label(top_frame, text="Sistema De Base De Datos Silvia Craft Store",
                                font=("Georga", 30, "bold"),
                                foreground="white",
                                background="dark turquoise")
        label_top_frame.place(x=175, y=5)

        label_name = Label(root, text="Nombre Completo:",
                           font=("Comic Sans", 20),
                           bg="DarkOrchid4",
                           fg="white")
        label_name.place(x=40, y=100)

        label_phone_number = Label(root, text="Numero De Telefono:",
                                   font=("Comic Sans", 20),
                                   bg="DarkOrchid4",
                                   fg="white")
        label_phone_number.place(x=40, y=160)

        label_city = Label(root, text="Ciudad R.D:",
                           font=("Comic Sans", 20),
                           bg="DarkOrchid4",
                           fg="white")
        label_city.place(x=650, y=100)

        label_adress = Label(root, text="Direccion Casa:",
                             font=("Comic Sans", 20),
                             bg="DarkOrchid4",
                             fg="white")
        label_adress.place(x=650, y=160)

        entry_name = Entry(root, font=("Roboto", 18),
                           foreground="red",
                           state="normal",
                           highlightbackground="gray",
                           highlightcolor="gray",
                           highlightthickness=2)
        entry_name.place(x=340, y=100)

        entry_phone_number = Entry(root, font=("font family", 18),
                                   foreground="red",
                                   highlightbackground="gray",
                                   highlightcolor="gray",
                                   highlightthickness=2)
        entry_phone_number.place(x=340, y=160)

        entry_city = Entry(root, font=("font family", 18),
                           foreground="red",
                           highlightbackground="gray",
                           highlightcolor="gray",
                           highlightthickness=2)
        entry_city.place(x=850, y=100)

        entry_adress = Entry(root, font=("Roboto", 18),
                             foreground="red",
                             highlightbackground="gray",
                             highlightcolor="gray",
                             highlightthickness=2)
        entry_adress.place(x=855, y=160)

        # crear el TreeView o el campo donde se van a almacenar los datos
        treeview = ttk.Treeview(root, columns=('ID', 'Nombre', 'Telefono', 'Ciudad', "Direccion"), show='headings')
        treeview.column('ID', width=50, anchor='center', stretch=False)
        treeview.column('Nombre', width=150, anchor='center', stretch=True)
        treeview.column('Telefono', width=150, anchor='center', stretch=True)
        treeview.column('Ciudad', width=160, anchor='center', stretch=True)
        treeview.column('Direccion', width=160, anchor='center', stretch=True)

        treeview.heading('#1', text='ID', anchor='center')
        treeview.heading('#2', text='Nombre', anchor='center')
        treeview.heading('#3', text='Celular', anchor='center')
        treeview.heading('#4', text='Ciudad', anchor='center')
        treeview.heading('#5', text='Direccion', anchor='center')
        treeview.place(x=0, y=250, width=1300)

        # funcion para eliminar un cliente de la base de datos
        def delete_client():
            messagebox.showwarning("information", "esta segura de que desea eliminar el cliente?")
            seleccion = treeview.selection()
            if seleccion:
                id = treeview.item(seleccion[0], "text")

                c.execute("DELETE FROM texto WHERE nombre=?", (entry_name.get(),))
                conn.commit()
                treeview.delete(seleccion[0])
                root.after(0, delete_client())
                root.update()

        # función para cargar los datos de la base de datos en el TreeView
        def load_data():
            # borrar los elementos actuales del TreeView
            for row in treeview.get_children():
                treeview.delete(row)

            # obtener los datos de la base de datos
            c.execute("SELECT * FROM texto ORDER BY nombre")
            resultado = c.fetchall()

            # agregar los datos al TreeView
            for row in resultado:
                treeview.insert('', END, values=row)

        load_data()

        # leer los datos introducidos
        def Save_Data():
            name = entry_name.get()
            phone_number = entry_phone_number.get()
            city = entry_city.get()
            adress = entry_adress.get()

            # mostrar un mensaje de error si todos los campos se quedan vacios
            if name == "" and phone_number == "" and city == "" and adress == "":
                messagebox.showerror("Error", "los campos no deben estar vacios")
            else:
                c.execute("INSERT INTO texto (nombre, telefono, ciudad, direccion) VALUES (?, ?, ?, ?)",
                      (name, phone_number, city, adress))
                conn.commit()

                # obtener el ID del nuevo registro
                id = c.lastrowid

                # agregar el nuevo registro al TreeView
                treeview.insert('', END, values=(id, name, phone_number, city, adress))

                # borrar el texto de los entries correspondientes
                entry_name.delete(0, END)
                entry_phone_number.delete(0, END)
                entry_city.delete(0, END)
                entry_adress.delete(0, END)
                messagebox.showinfo("information", "Datos guardados exitosamente a silvia craft store database!")
                root.after(0, load_data())
                root.update()

        image_add_user = PhotoImage(file="images/add1.png")
        Btn_add_user_to_db = Button(root, text="Agregar Cliente",
                                    font=("Roboto", 17, "bold"),
                                    background="dark turquoise",
                                    image=image_add_user,
                                    compound="right",
                                    command=Save_Data,
                                    state="normal")
        Btn_add_user_to_db.place(x=10, y=520)

        image_delete_client = PhotoImage(file="images/delete.png")
        Btn_delete_user_to_db = Button(root, text="Eliminar Cliente",
                                    font=("Roboto", 16, "bold"),
                                    background="dark turquoise",
                                    image=image_delete_client,
                                    compound="right",
                                    command=delete_client)
        Btn_delete_user_to_db.place(x=280, y=520)
        root.mainloop()

    else:
        messagebox.showerror("error", "Usted no esta autorizado para acceder a silvia craft store database!")


label_city = Label(main_window, text="Username",
                   font=("Comic Sans", 20),
                   fg="red")
label_city.pack()

entry_username = Entry(main_window, font=("Roboto", 18),
                       foreground="green",
                       highlightbackground="gray",
                       highlightcolor="gray",
                       highlightthickness=2)
entry_username.pack()

label_city = Label(main_window, text="Password",
                   font=("Comic Sans", 20),
                   fg="red")
label_city.pack()

entry_password = Entry(main_window, font=("Roboto", 18),
                       foreground="green",
                       highlightbackground="gray",
                       highlightcolor="gray",
                       highlightthickness=2,
                       show="*")
entry_password.pack()

Log_in_image = PhotoImage(file="images/log in.png")
Btn_sing_in = Button(main_window, text="Log In",
                            font=("Roboto", 17, "bold"),
                            image=Log_in_image,
                            compound="right",
                            background="dark turquoise",
                            command=next_window)
Btn_sing_in.place(x=70, y=180)

main_window.mainloop()