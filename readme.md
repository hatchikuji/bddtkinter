# Gestionnaire de Base de Données avec Interface Tkinter

Ce projet est une application de gestion de base de données avec une interface utilisateur graphique développée en Python en utilisant la bibliothèque Tkinter. Il permet d'interagir avec plusieurs tables dans une base de données MySQL, notamment `client`, `entreprise`, et `particulier`.

## Fonctionnalités

- **Insertion de données** : Ajouter de nouveaux enregistrements dans les tables `client`, `entreprise` et `particulier`.
- **Suppression de données** : Supprimer des enregistrements existants dans les tables.
- **Affichage des données** : Afficher les enregistrements des tables avec tous leurs attributs.
- **Exécution de requêtes SQL personnalisées** : Fournir une zone pour entrer et exécuter des requêtes SQL arbitraires.

## Prérequis

Avant de commencer, assurez-vous d'avoir :

- Python 3.8 ou une version ultérieure installée.
- Une base de données MySQL opérationnelle avec les tables suivantes créées :
    - `client`
      ```sql
      CREATE TABLE client (
          id_client INT AUTO_INCREMENT PRIMARY KEY,
          nom VARCHAR(255),
          prenom VARCHAR(255),
          date DATE,
          type VARCHAR(50),
          reseau_sociaux VARCHAR(255),
          code_postal VARCHAR(10),
          ville VARCHAR(255),
          mail VARCHAR(255),
          tel VARCHAR(15)
      );
      ```
    - `entreprise`
      ```sql
      CREATE TABLE entreprise (
          id_entreprise INT AUTO_INCREMENT PRIMARY KEY,
          reseau_sociaux VARCHAR(255),
          code_postal VARCHAR(10),
          ville VARCHAR(255)
      );
      ```
    - `particulier`
      ```sql
      CREATE TABLE particulier (
          id_particulier INT AUTO_INCREMENT PRIMARY KEY,
          mail VARCHAR(255),
          tel VARCHAR(15)
      );
      ```
- La bibliothèque Python `pymysql` installée :
  ```bash
  pip install pymysql

## Installation
Clonez ce dépôt sur votre machine locale :
```bash
git clone https://github.com/votre-utilisateur/bddtkinter.git
```
Accédez au répertoire du projet :
```bash 
cd votre-projet
```
Assurez-vous que le fichier de configuration de la base de données (config) contient les informations correctes pour se connecter à votre base de données MySQL.
## Utilisation
Lancez le script principal :
```bash 
python main.py
```
Une fenêtre s'ouvrira avec plusieurs onglets :
- 
- Client : Permet d'insérer, supprimer et afficher les clients.
- Entreprise : Permet d'insérer, supprimer et afficher les entreprises.
- Particulier : Permet d'insérer, supprimer et afficher les particuliers.
- Requêtes : Fournit une zone pour exécuter des requêtes SQL personnalisées.

Arborescence du projet
```lua
projet/
├── main.py
├── config.py
├── mysql.log
├── README.md
└── requirements.txt
```
- main.py : Script principal contenant l'interface utilisateur et les fonctions.
- config.py : Fichier contenant les informations de configuration pour se connecter à la base de données.
- mysql.log : Fichier journal pour enregistrer les événements liés à la base de données.
- README.md : Documentation du projet.
- requirements.txt : Liste des dépendances nécessaires.

## Journalisation
Tous les événements importants (connexion à la base, erreurs SQL, etc.) sont enregistrés dans le fichier mysql.log pour simplifier le débogage.

## Auteur
Projet développé par Swann Brillant.

## Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser, de le modifier et de le distribuer.