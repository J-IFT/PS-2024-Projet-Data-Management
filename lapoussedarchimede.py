from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import csv
import argparse

# Création du moteur de base de données (ATTENTION MODIFIEZ BIEN LE PATH POUR QUE CA FONCTIONNE)
engine = create_engine('sqlite:///C:/Users/julie/OneDrive - Ifag Paris/Documents/Data Management/projet/PS-2024-Projet-Data-Management/lapoussedarchimede.db', echo=True)
Base = declarative_base()

class Plante(Base):
    __tablename__ = 'plante'

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    hauteur = Column(Integer)
    date_entree = Column(Date)
    date_mort = Column(Date, nullable=True)
    famille_nom = Column(String, ForeignKey('famille.nom'))
    origine_nom = Column(String, ForeignKey('origine.nom'))
    periode_floraison_nom = Column(String, ForeignKey('periode_floraison.nom'))
    type_sol_nom = Column(String, ForeignKey('type_sol.nom'))
    exposition_nom = Column(String, ForeignKey('exposition.nom'))
    etat_sante_nom = Column(String, ForeignKey('etat_sante.nom'))
    type_nom = Column(String, ForeignKey('type.nom'))

    famille = relationship("Famille", back_populates="plantes")
    origine = relationship("Origine", back_populates="plantes")
    periode_floraison = relationship("PeriodeFloraison", back_populates="plantes")
    type_sol = relationship("TypeSol", back_populates="plantes")
    exposition = relationship("Exposition", back_populates="plantes")
    etat_sante = relationship("EtatSante", back_populates="plantes")
    type = relationship("Type", back_populates="plantes")

class Famille(Base):
    __tablename__ = 'famille'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="famille")

class Origine(Base):
    __tablename__ = 'origine'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="origine")

class PeriodeFloraison(Base):
    __tablename__ = 'periode_floraison'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="periode_floraison")

class TypeSol(Base):
    __tablename__ = 'type_sol'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="type_sol")

class Exposition(Base):
    __tablename__ = 'exposition'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="exposition")

class EtatSante(Base):
    __tablename__ = 'etat_sante'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="etat_sante")

class Type(Base):
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    nom = Column(String)

    plantes = relationship("Plante", back_populates="type")

# Création des tables dans la base de données
Base.metadata.create_all(engine)

# Insérer des valeurs uniques dans chaque table
Session = sessionmaker(bind=engine)
session = Session()

# Insérer des valeurs uniques dans la table Famille
familles = ["Rosacées", "Orchidacées", "Liliacées", "Astéracées", "Amaryllidacées",
            "Nelumbonacées", "Lamiacées", "Papaveracées", "Iridacées", "Oléacées",
            "Paeoniacées", "Boraginacées", "Géraniacées", "Hydrangeacées", "Caryophyllacées",
            "Violacées", "Éricacées", "Caprifoliacées", "Hippocastanacées", "Buxacées",
            "Berbéridacées", "Fagacées", "Acéracées", "Pinacées", "Cupressacées",
            "Platanacées", "Salicacées", "Buxacées", "Théacées"]
for famille_nom in familles:
    famille = Famille(nom=famille_nom)
    session.add(famille)

# Insérer des valeurs uniques dans la table Origine
origines = ["Europe", "Asie", "Amérique", "Amérique du Nord", "Méditerranée"]
for origine_nom in origines:
    origine = Origine(nom=origine_nom)
    session.add(origine)

# Insérer des valeurs uniques dans la table PeriodeFloraison
periodes_floraison = ["Été", "Printemps", "Hiver", "Automne"]
for periode_nom in periodes_floraison:
    periode = PeriodeFloraison(nom=periode_nom)
    session.add(periode)

# Insérer des valeurs uniques dans la table TypeSol
types_sol = ["Argileux", "Humifère", "Sableux"]
for type_sol_nom in types_sol:
    type_sol = TypeSol(nom=type_sol_nom)
    session.add(type_sol)

# Insérer des valeurs uniques dans la table Exposition
expositions = ["Ensoleillée", "Mi-ombragée"]
for exposition_nom in expositions:
    exposition = Exposition(nom=exposition_nom)
    session.add(exposition)

# Insérer des valeurs uniques dans la table EtatSante
etats_sante = ["Bon", "Excellent", "Très bon"]
for etat_sante_nom in etats_sante:
    etat_sante = EtatSante(nom=etat_sante_nom)
    session.add(etat_sante)

# Insérer des valeurs uniques dans la table Type
types = ["Fleur", "Arbuste", "Arbre"]
for type_nom in types:
    type_ = Type(nom=type_nom)
    session.add(type_)

# Chemin vers le fichier CSV (Assurez-vous de remplacer le chemin du fichier)
fichier_csv = "la_Pousse_dArchemede.csv"

# Lecture du fichier CSV et insertion des plantes dans la base de données
with open(fichier_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  # Ignorer l'en-tête
    for row in reader:
        nom = row[1].strip()
        hauteur = float(row[4].replace(',', '.'))
        date_entree = datetime.strptime(row[8].strip(), '%Y-%m-%d').date()
        date_mort = None
        if row[9].strip():
            date_mort = datetime.strptime(row[9].strip(), '%Y-%m-%d').date()
        famille_nom = row[2].strip()
        origine_nom = row[3].strip()
        periode_floraison_nom = row[5].strip()
        type_sol_nom = row[6].strip()
        exposition_nom = row[7].strip()
        etat_sante_nom = row[10].strip()
        type_nom = row[11].strip()

        plante = Plante(nom=nom, hauteur=hauteur, date_entree=date_entree,
                        famille_nom=famille_nom, origine_nom=origine_nom,
                        periode_floraison_nom=periode_floraison_nom,
                        type_sol_nom=type_sol_nom, exposition_nom=exposition_nom,
                        etat_sante_nom=etat_sante_nom, type_nom=type_nom)

        # Ajoutez la plante à la session et committez
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(plante.__table__.insert(), {
                    'nom': plante.nom,
                    'hauteur': plante.hauteur,
                    'date_entree': plante.date_entree,
                    'famille_nom': plante.famille_nom,
                    'origine_nom': plante.origine_nom,
                    'periode_floraison_nom': plante.periode_floraison_nom,
                    'type_sol_nom': plante.type_sol_nom,
                    'exposition_nom': plante.exposition_nom,
                    'etat_sante_nom': plante.etat_sante_nom,
                    'type_nom': plante.type_nom
                })

# Menu CRUD
while True:
    print("\nMenu:")
    print("1. Ajouter une plante")
    print("2. Lire les plantes")
    print("3. Modifier une plante")
    print("4. Supprimer une plante")
    print("5. Quitter")

    choix = input("Entrez le numéro de l'opération que vous souhaitez effectuer : ")

    if choix == "1":
        # Code pour ajouter une plante
        nom = input("Entrez le nom de la plante : ")
        hauteur = float(input("Entrez la hauteur de la plante : "))
        date_entree = datetime.strptime(input("Entrez la date d'entrée de la plante (YYYY-MM-DD) : "), '%Y-%m-%d').date()
        date_mort = datetime.strptime(input("Entrez la date de mort de la plante (YYYY-MM-DD) : "), '%Y-%m-%d').date()
        famille_nom = input("Entrez le nom de la famille de la plante : ")
        origine_nom = input("Entrez le nom de l'origine de la plante : ")
        periode_floraison_nom = input("Entrez le nom de la période de floraison de la plante : ")
        type_sol_nom = input("Entrez le nom du type de sol de la plante : ")
        exposition_nom = input("Entrez le nom de l'exposition de la plante : ")
        etat_sante_nom = input("Entrez le nom de l'état de santé de la plante : ")
        type_nom = input("Entrez le nom du type de la plante : ")
        plante = Plante(nom=nom, hauteur=hauteur, date_entree=date_entree, date_mort=date_mort,
                        famille_nom=famille_nom, origine_nom=origine_nom, periode_floraison_nom=periode_floraison_nom,
                        type_sol_nom=type_sol_nom, exposition_nom=exposition_nom, etat_sante_nom=etat_sante_nom,
                        type_nom=type_nom)
        session.add(plante)
        session.commit()
        print("Plante ajoutée avec succès !")
    elif choix == "2":
        # Code pour lire les plantes
        print("Liste des plantes :")
        for plante in session.query(Plante).all():
            print(f"ID : {plante.id}, Nom : {plante.nom}, Hauteur : {plante.hauteur}, Date d'entrée : {plante.date_entree}")
    elif choix == "3":
        # Code pour modifier une plante
        nom = input("Entrez le nom de la plante à modifier : ")
        hauteur = float(input("Entrez la nouvelle hauteur de la plante : "))
        date_entree = datetime.strptime(input("Entrez la nouvelle date d'entrée de la plante (YYYY-MM-DD) : "), '%Y-%m-%d').date()
        date_mort = datetime.strptime(input("Entrez la nouvelle date de mort de la plante (YYYY-MM-DD) : "), '%Y-%m-%d').date()
        famille_nom = input("Entrez le nouveau nom de la famille de la plante : ")
        origine_nom = input("Entrez le nouveau nom de l'origine de la plante : ")
        periode_floraison_nom = input("Entrez le nouveau nom de la période de floraison de la plante : ")
        type_sol_nom = input("Entrez le nouveau nom du type de sol de la plante : ")
        exposition_nom = input("Entrez le nouveau nom de l'exposition de la plante : ")
        etat_sante_nom = input("Entrez le nouveau nom de l'état de santé de la plante : ")
        type_nom = input("Entrez le nouveau nom du type de la plante : ")
        plante = session.query(Plante).filter_by(nom=nom).first()
        if plante:
            plante.hauteur = hauteur
            plante.date_entree = date_entree
            plante.date_mort = date_mort
            plante.famille_nom = famille_nom
            plante.origine_nom = origine_nom
            plante.periode_floraison_nom = periode_floraison_nom
            plante.type_sol_nom = type_sol_nom
            plante.exposition_nom = exposition_nom
            plante.etat_sante_nom = etat_sante_nom
            plante.type_nom = type_nom
            session.commit()
            print("Plante modifiée avec succès !")
        else:
            print("Plante non trouvée.")
    elif choix == "4":
        # Code pour supprimer une plante
        nom = input("Entrez le nom de la plante à supprimer : ")
        plante = session.query(Plante).filter_by(nom=nom).first()
        if plante:
            session.delete(plante)
            session.commit()
            print("Plante supprimée avec succès !")
        else:
            print("Plante non trouvée.")
    elif choix == "5":
        # Quitter le menu
        print("Merci d'avoir utilisé le programme. Au revoir !")
        break
    else:
        print("Choix invalide. Veuillez entrer un numéro valide.")

# Commit des changements
session.commit()

# Fermeture de la session
session.close()
