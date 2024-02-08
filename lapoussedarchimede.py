from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Création du moteur de base de données (ATTENTION MODIFIEZ BIEN LE PATH POUR QUE CA FONCTIONNE)
engine = create_engine('sqlite:///C:/Users/julie\OneDrive - Ifag Paris/Documents/Data Management/projet/PS-2024-Projet-Data-Management/lapoussedarchimede.db', echo=True)
Base = declarative_base()

class Plante(Base):
    __tablename__ = 'plante'

    id = Column(Integer, primary_key=True)
    nom = Column(String)
    hauteur = Column(Integer)
    date_entree = Column(Date)
    date_mort = Column(Date)

    famille_id = Column(Integer, ForeignKey('famille.id'))
    origine_id = Column(Integer, ForeignKey('origine.id'))
    periode_floraison_id = Column(Integer, ForeignKey('periode_floraison.id'))
    type_sol_id = Column(Integer, ForeignKey('type_sol.id'))
    exposition_id = Column(Integer, ForeignKey('exposition.id'))
    etat_sante_id = Column(Integer, ForeignKey('etat_sante.id'))
    type_id = Column(Integer, ForeignKey('type.id'))

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
