import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

CSV_FILE = "suivi_taches.csv"
COLLABORATEURS = [f"Collaborateur {i+1}" for i in range(9)]
TYPES_TACHES = ["Analyse ad-hoc", "Support", "Veille concurrentielle", "Formation", "Réunion projet interne", "Autre"]

def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Collaborateur", "Type de tâche", "Description", "Temps passé (heures)"])

def load_data():
    for item in tree.get_children():
        tree.delete(item)
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                tree.insert("", "end", values=row)

def add_task():
    date = entry_date.get()
    collab = combo_collab.get()
    type_tache = combo_type.get()
    desc = entry_desc.get()
    temps = entry_temps.get()

    if not date or not collab or not type_tache or not desc or not temps:
        messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
        return

    try:
        float(temps)
    except ValueError:
        messagebox.showwarning("Erreur", "Le temps passé doit être un nombre valide.")
        return

    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date, collab, type_tache, desc, temps])

    load_data()

    # Reset fields
    entry_desc.delete(0, tk.END)
    entry_temps.delete(0, tk.END)
    messagebox.showinfo("Succès", "Tâche ajoutée avec succès !")

# Init GUI
root = tk.Tk()
root.title("Suivi des Tâches Non Comptabilisées")
root.geometry("800x600")

init_csv()

# Formulaire
frame_form = tk.LabelFrame(root, text="Ajouter une nouvelle tâche", padx=10, pady=10)
frame_form.pack(fill="x", padx=10, pady=10)

tk.Label(frame_form, text="Date (JJ/MM/AAAA):").grid(row=0, column=0, sticky="w", pady=5)
entry_date = tk.Entry(frame_form)
entry_date.insert(0, datetime.today().strftime('%d/%m/%Y'))
entry_date.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Collaborateur:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
combo_collab = ttk.Combobox(frame_form, values=COLLABORATEURS, state="readonly")
combo_collab.current(0)
combo_collab.grid(row=0, column=3, pady=5)

tk.Label(frame_form, text="Type de tâche:").grid(row=1, column=0, sticky="w", pady=5)
combo_type = ttk.Combobox(frame_form, values=TYPES_TACHES, state="readonly")
combo_type.current(0)
combo_type.grid(row=1, column=1, pady=5, padx=5)

tk.Label(frame_form, text="Temps passé (h):").grid(row=1, column=2, sticky="w", pady=5, padx=5)
entry_temps = tk.Entry(frame_form)
entry_temps.grid(row=1, column=3, pady=5)

tk.Label(frame_form, text="Description:").grid(row=2, column=0, sticky="w", pady=5)
entry_desc = tk.Entry(frame_form, width=50)
entry_desc.grid(row=2, column=1, columnspan=3, sticky="w", pady=5, padx=5)

btn_add = tk.Button(frame_form, text="Ajouter la tâche", command=add_task, bg="lightblue")
btn_add.grid(row=3, column=0, columnspan=4, pady=10)

# Tableau d'historique
frame_tree = tk.LabelFrame(root, text="Historique des tâches", padx=10, pady=10)
frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Date", "Collaborateur", "Type de tâche", "Description", "Temps (h)")
tree = ttk.Treeview(frame_tree, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True, side="left")

scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

load_data()

root.mainloop()
