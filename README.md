# SuperOrga

SuperOrga est un outil de génération d'organigrammes pour les entreprises.

## Structure

La structure de l'organigramme est la suivante :
    
    levels: 
    - grades:
     - title: "Patron"
      image: "images/patron.png"
      subtitle: "Directeur général"
      connect_horizontal: True  #  option pour la connexion horizontale
    - grades:
      - title: "Apprenti"
        image: "images/apprenti.png"
        subtitle: "Stagiaire en formation"
    connections:
    - from: "Patron"
      to: ["Apprenti"]  # Connexion explicite du Patron vers Apprenti


## Description

SuperOrga est un outil de génération d'organigrammes pour les entreprises. Il permet de créer des organigrammes de manière simple et intuitive. Il suffit de définir les différents niveaux de l'organigramme, les grades et les connexions entre les différents niveaux. SuperOrga se charge ensuite de générer l'organigramme correspondant.
