import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import pymysql
import logging
import c

config = c.config

# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

file_handler = logging.FileHandler('mysql.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def connect_db(config):
    try:
        return pymysql.connect(**config)
    except pymysql.MySQLError as e:
        logger.error("Erreur de connexion à la base de données: %s", e)
        return None

def load_data(treeview, get_data_function):
    # Supprimer les anciens enregistrements de la vue
    for item in treeview.get_children():
        treeview.delete(item)

    # Charger les nouveaux enregistrements
    records = get_data_function()
    for record in records:
        treeview.insert("", "end", values=record)

#------------------------------------------------------------------------------------#
# FONCTIONS
# POUR
# LES AJOUTS / SUPPRESSIONS / RECUPERATIONS
#------------------------------------------------------------------------------------#

# FONCTIONS POUR LES REQUÊTES PUR SQL

def query_request(query):
    cnx = connect_db(config)
    if cnx is None:
        return "Erreur de connexion à la base de données."

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query)
            if query.strip().lower().startswith("select"):
                # Si c'est une requête SELECT, récupérer les données
                rows = cursor.fetchall()
                if not rows:
                    return "Aucune donnée trouvée."

                # Formater les résultats pour un affichage correct
                result = "\n".join([str(row) for row in rows])
                return result
            else:
                cnx.commit()  # Pour les requêtes d'insertion ou de modification
                return "Requête exécutée avec succès."
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la requête: %s", e)
        return f"Erreur lors de la requête: {e}"
    finally:
        cnx.close()

def execute_query():
    query = query_entry.get("1.0", tk.END).strip()  # Récupérer la requête
    if query:
        result = query_request(query)  # Exécuter la requête
        result_label.config(text=result)

# FONCTIONS POUR LES CLIENTS

def insert_client(nom, prenom, date, client_type, reseau_sociaux, code_postal, ville, mail, tel):
    query = """
    INSERT INTO client (nom, prenom, date, type, reseau_sociaux, code_postal, ville, mail, tel)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (nom, prenom, date, client_type, reseau_sociaux, code_postal, ville, mail, tel)

    cnx = connect_db(config)
    if cnx is None:
        return "Erreur de connexion à la base de données."

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query, values)
            cnx.commit()
            return "Insertion réussie."
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de l'insertion: %s", e)
        return f"Erreur lors de l'insertion: {e}"
    finally:
        cnx.close()

def execute_insert_client():
    result = insert_client(
        client_nom_entry.get(),
        client_prenom_entry.get(),
        client_date_entry.get(),
        client_type_entry.get(),
        client_reseau_entry.get(),
        client_code_postal_entry.get(),
        client_ville_entry.get(),
        client_mail_entry.get(),
        client_tel_entry.get()
    )
    messagebox.showinfo("Résultat", result)

def delete_client(criteria, value):
    query = f"DELETE FROM client WHERE {criteria} = %s"

    cnx = connect_db(config)
    if cnx is None:
        return "Erreur de connexion à la base de données."

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query, (value,))
            cnx.commit()
            return "Suppression réussie."
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la suppression: %s", e)
        return f"Erreur lors de la suppression: {e}"
    finally:
        cnx.close()

def execute_delete_client():
    result = delete_client(client_delete_criteria.get(), client_delete_value.get())
    messagebox.showinfo("Résultat", result)
    
def get_all_clients():
    query = "SELECT id_client, nom, prenom, date, type, reseau_sociaux, code_postal, ville, mail, tel FROM client"

    cnx = connect_db(config)
    if cnx is None:
        return []

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la récupération des clients: %s", e)
        return []
    finally:
        cnx.close()

def load_clients():
    # Supprimer les anciens clients de la vue
    for item in clients_tree.get_children():
        clients_tree.delete(item)

    # Charger les nouveaux clients
    clients = get_all_clients()
    for client in clients:
        clients_tree.insert("", "end", values=client)

# FONCTION POUR LES ENTREPRISES

def delete_entreprise(criteria, value):
    query = f"DELETE FROM entreprise WHERE {criteria} = %s"

    cnx = connect_db(config)
    if cnx is None:
        return "Erreur de connexion à la base de données."

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query, (value,))
            cnx.commit()
            return "Suppression réussie."
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la suppression: %s", e)
        return f"Erreur lors de la suppression: {e}"
    finally:
        cnx.close()

def execute_delete_entreprise():
    result = delete_entreprise(entreprise_delete_criteria.get(), entreprise_delete_value.get())
    messagebox.showinfo("Résultat", result)

def get_all_entreprises():
    query = "SELECT id_entreprise, reseau_sociaux, code_postal, ville FROM entreprise"

    cnx = connect_db(config)
    if cnx is None:
        return []

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la récupération des entreprises: %s", e)
        return []
    finally:
        cnx.close()

def load_entreprises():
    # Supprimer les anciennes entreprises de la vue
    for item in entreprises_tree.get_children():
        entreprises_tree.delete(item)
    
    # Charger les nouvelles entreprises
    entreprises = get_all_entreprises()
    for ent in entreprises:
        entreprises_tree.insert("", "end", values=ent)

# FONCTION POUR LES PARTICULIERS

def delete_particulier(criteria, value):
    query = f"DELETE FROM particulier WHERE {criteria} = %s"

    cnx = connect_db(config)
    if cnx is None:
        return "Erreur de connexion à la base de données."

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query, (value,))
            cnx.commit()
            return "Suppression réussie."
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la suppression: %s", e)
        return f"Erreur lors de la suppression: {e}"
    finally:
        cnx.close()

def execute_delete_particulier():
    result = delete_particulier(particulier_delete_criteria.get(), particulier_delete_value.get())
    messagebox.showinfo("Résultat", result)

def get_all_particuliers():
    query = "SELECT id_particulier, mail, tel FROM particulier"

    cnx = connect_db(config)
    if cnx is None:
        return []

    try:
        with cnx.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
    except pymysql.MySQLError as e:
        logger.error("Erreur lors de la récupération des particuliers: %s", e)
        return []
    finally:
        cnx.close()

def load_particuliers():
    # Supprimer les anciens particuliers de la vue
    for item in particulier_tree.get_children():
        particulier_tree.delete(item)
    
    #charger les nouveaux particuliers
    particuliers = get_all_particuliers()
    for particuliers in particuliers:
        particulier_tree.insert("", "end", values=particuliers)

# Création de la fenêtre Tkinter
root = tk.Tk()
root.title("Gestion de Base de Données")

# Création des onglets
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

#------------------------------------------------------------------------------------#
# FRAME
# POUR
# CLIENT / ENTREPRISES / PARTICULIERS
# ------------------------------------------------------------------------------------#
# Frame pour faire ques requêtes SQL
query_frame = ttk.Frame(notebook,width=400, height=400)
query_frame.pack(fill=tk.BOTH, expand=True)

# ------------------------------------------------------------------------------------#
# Frame pour l'onglet Inserer des Clients
insert_client_frame = ttk.Frame(notebook, width=400, height=400)
insert_client_frame.pack(fill='both', expand=True)

# Frame pour l'onglet Suppression des Clients
delete_client_frame = ttk.Frame(notebook, width=400, height=400)
delete_client_frame.pack(fill='both', expand=True)

# Frame pour l'onglet Liste des Clients
list_client_frame = ttk.Frame(notebook, width=400, height=400)
list_client_frame.pack(fill='both', expand=True)
#------------------------------------------------------------------------------------#
# Frame pour l'onglet Suppression d'une entreprise
delete_entreprise_frame = ttk.Frame(notebook, width=400, height=400)
delete_entreprise_frame.pack(fill='both', expand=True)

# Frame pour l'onglet Liste des entreprises
list_entreprise_frame = ttk.Frame(notebook, width=400, height=400)
list_entreprise_frame.pack(fill='both', expand=True)
#------------------------------------------------------------------------------------#
# Frame pour l'onglet Suppression d'un particulier
delete_particulier_frame = ttk.Frame(notebook, width=400, height=400)
delete_particulier_frame.pack(fill='both', expand=True)

# Frame pour l'onglet Liste des particuliers
list_particulier_frame = ttk.Frame(notebook, width=400, height=400)
list_particulier_frame.pack(fill='both', expand=True)
#------------------------------------------------------------------------------------#
# Ajout des onglets
notebook.add(query_frame, text="Requêtes")
notebook.add(insert_client_frame, text="Insertion Clients")
notebook.add(delete_client_frame, text="Suppression Clients")
notebook.add(list_client_frame, text="Liste des Clients")
notebook.add(delete_entreprise_frame, text="Suppression Entreprise")
notebook.add(list_entreprise_frame, text="Liste des Entreprises")
notebook.add(delete_particulier_frame, text="Suppression Particulier")
notebook.add(list_particulier_frame, text="Liste des Particuliers")

#-----------------------------------------------------------------------------------#
# FENETRE
# POUR
# LES REQUETES
#-----------------------------------------------------------------------------------#

tk.Label(query_frame, text="Entrez votre requête SQL:").pack(pady=10)
query_entry = tk.Text(query_frame, height=10, width=50)
query_entry.pack(pady=10)
result_label = tk.Label(query_frame, text="", wraplength=400, justify=tk.LEFT)
result_label.pack(pady=10)

execute_button = tk.Button(query_frame, text="Exécuter", command=execute_query)
execute_button.pack(pady=10)

#-----------------------------------------------------------------------------------#
# FENETRE
# POUR
# LES CLIENTS
#-----------------------------------------------------------------------------------#

#Insertion des clients dans la bdd

tk.Label(insert_client_frame, text="Nom:").pack()
client_nom_entry = tk.Entry(insert_client_frame)
client_nom_entry.pack()

tk.Label(insert_client_frame, text="Prénom:").pack()
client_prenom_entry = tk.Entry(insert_client_frame)
client_prenom_entry.pack()

tk.Label(insert_client_frame, text="Date (YYYY-MM-DD):").pack()
client_date_entry = tk.Entry(insert_client_frame)
client_date_entry.pack()

tk.Label(insert_client_frame, text="Type:").pack()
client_type_entry = tk.Entry(insert_client_frame)
client_type_entry.pack()

tk.Label(insert_client_frame, text="Réseau Social:").pack()
client_reseau_entry = tk.Entry(insert_client_frame)
client_reseau_entry.pack()

tk.Label(insert_client_frame, text="Code Postal:").pack()
client_code_postal_entry = tk.Entry(insert_client_frame)
client_code_postal_entry.pack()

tk.Label(insert_client_frame, text="Ville:").pack()
client_ville_entry = tk.Entry(insert_client_frame)
client_ville_entry.pack()

tk.Label(insert_client_frame, text="Email:").pack()
client_mail_entry = tk.Entry(insert_client_frame)
client_mail_entry.pack()

tk.Label(insert_client_frame, text="Téléphone:").pack()
client_tel_entry = tk.Entry(insert_client_frame)
client_tel_entry.pack()

client_insert_button = tk.Button(insert_client_frame, text="Insérer le Client", command=execute_insert_client)
client_insert_button.pack(pady=10)

#-----------------------------------------------------------------------------------#
#
# Contenu de l'onglet Suppression Client
#
#-----------------------------------------------------------------------------------#

tk.Label(delete_client_frame, text="Critère de suppression (mail, tel, etc.):").pack()
client_delete_criteria = tk.Entry(delete_client_frame)
client_delete_criteria.pack()

tk.Label(delete_client_frame, text="Valeur du critère:").pack()
client_delete_value = tk.Entry(delete_client_frame)
client_delete_value.pack()

client_delete_button = tk.Button(delete_client_frame, text="Supprimer le Client", command=execute_delete_client)
client_delete_button.pack(pady=10)

#-----------------------------------------------------------------------------------#
#
# Contenu de l'onglet Visualisation Client
#
#-----------------------------------------------------------------------------------#

clients_tree = ttk.Treeview(list_client_frame, columns=("ID", "Nom", "Prenom", "Date", "Type", "Reseau", "Code Postal", "Ville", "Email", "Telephone"), show='headings')

clients_tree.heading("ID", text="ID")
clients_tree.heading("Nom", text="Nom")
clients_tree.heading("Prenom", text="Prénom")
clients_tree.heading("Date", text="Date")
clients_tree.heading("Type", text="Type")
clients_tree.heading("Reseau", text="Réseau Social")
clients_tree.heading("Code Postal", text="Code Postal")
clients_tree.heading("Ville", text="Ville")
clients_tree.heading("Email", text="Email")
clients_tree.heading("Telephone", text="Téléphone")
clients_tree.pack(fill='both', expand=True)

# Bouton pour charger les clients
client_load_button = tk.Button(list_client_frame, text="Charger les Clients", command=load_clients)
client_load_button.pack(pady=10)

#------------------------------------------------------------------------------------#
# FENETRES
# LES
# ENTREPRISES
#------------------------------------------------------------------------------------#
# Contenu de l'onglet Suppression Entreprise


tk.Label(delete_entreprise_frame, text="Critère de suppression (Réseau Social, Code postal, etc.):").pack()
entreprise_delete_criteria = tk.Entry(delete_entreprise_frame)
entreprise_delete_criteria.pack()

tk.Label(delete_entreprise_frame, text="Valeur du critère:").pack()
entreprise_delete_value = tk.Entry(delete_entreprise_frame)
entreprise_delete_value.pack()

entreprise_delete_button = tk.Button(delete_entreprise_frame, text="Supprimer l'Entreprise", command= execute_delete_entreprise)
entreprise_delete_button.pack(pady=10)

#-----------------------------------------------------------------------------------#
#
# Contenu de l'onglet Visualisation Entreprises
#
#-----------------------------------------------------------------------------------#

# Contenu de l'onglet Liste des Entreprises
entreprises_tree = ttk.Treeview(list_entreprise_frame, columns=("ID Entreprise", "Réseau Social", "Code Postal", "Ville"), show='headings')

entreprises_tree.heading("ID Entreprise", text="ID Entreprise")
entreprises_tree.heading("Réseau Social", text="Réseau Social")
entreprises_tree.heading("Code Postal", text="Code Postal")
entreprises_tree.heading("Ville", text="Ville")
entreprises_tree.pack(fill='both', expand=True)

# Bouton pour charger les entreprises
entreprises_load_button = tk.Button(list_entreprise_frame, text="Charger les Entreprises", command=load_entreprises)
entreprises_load_button.pack(pady=10)

#------------------------------------------------------------------------------------#
# FENETRES
# LES
# PARTICULIERS
#------------------------------------------------------------------------------------#
# Contenu de l'onglet Suppression Particulier


tk.Label(delete_particulier_frame, text="Critère de suppression (Mail, Tel.):").pack()
particulier_delete_criteria = tk.Entry(delete_particulier_frame)
particulier_delete_criteria.pack()

tk.Label(delete_entreprise_frame, text="Valeur du critère:").pack()
particulier_delete_value = tk.Entry(delete_entreprise_frame)
particulier_delete_value.pack()

particulier_delete_button = tk.Button(delete_entreprise_frame, text="Supprimer l'Entreprise", command= execute_delete_particulier)
particulier_delete_button.pack(pady=10)

#-----------------------------------------------------------------------------------#
#
# Contenu de l'onglet Visualisation Particulier
#
#-----------------------------------------------------------------------------------#
# Contenu de l'onglet Liste des particuliers

particulier_tree = ttk.Treeview(list_particulier_frame, columns=("ID", "Mail", "Tel"), show='headings')

particulier_tree.heading("ID", text="ID")
particulier_tree.heading("Mail", text="Mail")
particulier_tree.heading("Tel", text="Tel")
particulier_tree.pack(fill='both', expand=True)

# Bouton pour charger les particuliers
particuliers_load_button = tk.Button(list_particulier_frame, text="Charger les Particuliers", command=load_particuliers)
particuliers_load_button.pack(pady=10)


# Boucle principale
root.mainloop()