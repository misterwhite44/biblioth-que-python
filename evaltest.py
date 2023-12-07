import json

# Patron de conception Factory
class Livre:
    def __init__(self, titre, auteur, categorie, est_disponible=True):  # Constructeur, je construis des objets
        self.titre = titre
        self.auteur = auteur
        self.categorie = categorie
        self.est_disponible = est_disponible

    def __str__(self):
        return f"{self.titre} par {self.auteur} ({self.categorie})" + (" (disponible)" if self.est_disponible else " (non disponible)")

class Utilisateur:  # Classe utilisateur
    def __init__(self, nom):
        self.nom = nom
        self.livres_empruntes = []

    def __str__(self):
        return f"Utilisateur : {self.nom}"

# Patron de conception Observer
class ObservateurLivre:  # Classe observateur
    def __init__(self):
        self.abonnes = []

    def s_abonner(self, abonne):
        self.abonnes.append(abonne)

    def se_desabonner(self, abonne):
        self.abonnes.remove(abonne)

    def notifier(self, livre):
        for abonne in self.abonnes:
            abonne.mettre_a_jour(livre)

# Patron de conception Strategy
class StrategieRecherche:
    def rechercher(self, mot_cle, elements):
        raise NotImplementedError("Les sous-classes doivent implémenter la méthode de recherche.")

class StrategieRechercheTitre(StrategieRecherche):  # Classe de recherche par titre
    def rechercher(self, mot_cle, elements):
        return [element for element in elements if mot_cle.lower() in element.titre.lower()]

class StrategieRechercheAuteur(StrategieRecherche):  # Classe de recherche par auteur
    def rechercher(self, mot_cle, elements):
        return [element for element in elements if mot_cle.lower() in element.auteur.lower()]

class StrategieRechercheCategorie(StrategieRecherche):  # Classe de recherche par catégorie
    def rechercher(self, mot_cle, elements):
        return [element for element in elements if mot_cle.lower() in element.categorie.lower()]

# Patron de conception Singleton
class Bibliotheque:  # Base de données pour mes différentes classes (livres, utilisateurs)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Bibliotheque, cls).__new__(cls)
            cls._instance.livres = []
            cls._instance.utilisateurs = []
            cls._instance.observateur = ObservateurLivre()
        return cls._instance

    def sauvegarder_etat(self, nom_fichier):
        donnees = {'livres': [livre.__dict__ for livre in self.livres],
                   'utilisateurs': [utilisateur.__dict__ for utilisateur in self.utilisateurs]}
        with open(nom_fichier, 'w') as fichier:
            json.dump(donnees, fichier, default=self.serialiser_instance)

    def charger_etat(self, nom_fichier):
        with open(nom_fichier, 'r') as fichier:
            donnees = json.load(fichier)
            self.livres = [Livre(**livre) for livre in donnees['livres']]
            self.utilisateurs = [Utilisateur(**utilisateur) for utilisateur in donnees['utilisateurs']]

    def ajouter_livre(self, livre):
        self.livres.append(livre)
        self.observateur.notifier(livre)

    def retirer_livre(self, livre):
        if livre in self.livres:
            self.livres.remove(livre)
        else:
            print("Livre non trouvé dans la bibliothèque.")

    def ajouter_utilisateur(self, utilisateur):
        self.utilisateurs.append(utilisateur)
        print(f"Utilisateur '{utilisateur.nom}' ajouté à la bibliothèque.")

    def emprunter_livre(self, utilisateur, livre):  # Emprunter un livre
        if livre.est_disponible:
            utilisateur.livres_empruntes.append(livre)
            livre.est_disponible = False
            print(f"{utilisateur.nom} a emprunté '{livre.titre}'.")
        else:
            print("Le livre n'est pas disponible.")

    def retourner_livre(self, utilisateur, livre):
        if livre in utilisateur.livres_empruntes:
            utilisateur.livres_empruntes.remove(livre)
            livre.est_disponible = True
            print(f"{utilisateur.nom} a retourné '{livre.titre}'.")
        else:
            print("Vous n'avez pas emprunté ce livre.")

    def afficher_tous_les_livres(self):
        print("Tous les livres dans la bibliothèque:")
        for livre in self.livres:
            print(livre)

    def afficher_tous_les_utilisateurs(self):
        print("Tous les utilisateurs dans la bibliothèque:")
        for utilisateur in self.utilisateurs:
            print(utilisateur)

    def rechercher_livres(self, strategie, mot_cle):
        resultats = strategie.rechercher(mot_cle, self.livres)
        print(f"Résultats de la recherche pour '{mot_cle}':")
        for resultat in resultats:
            print(resultat)

    def serialiser_instance(self, obj):
        if isinstance(obj, Livre) or isinstance(obj, Utilisateur):
            return obj.__dict__
        raise TypeError(f"Objet de type {obj.__class__.__name__} n'est pas sérialisable en JSON.")

# Créez une instance de la bibliothèque
db = Bibliotheque()
# Ajoutez quelques livres à la bibliothèque
db.ajouter_livre(Livre("L'epouvanteur", "Joseph Delaney", "Fantaisie"))
db.ajouter_livre(Livre("Autre Monde", "Maxime Chattam", "Fantaisie"))

# Ajoutez quelques utilisateurs
utilisateur1 = Utilisateur("Louis")
utilisateur2 = Utilisateur("Gilles")
db.ajouter_utilisateur(utilisateur1)
db.ajouter_utilisateur(utilisateur2)

# Exemple d'utilisation avec l'affichage de tous les livres en premier
db.afficher_tous_les_livres()

data = Bibliotheque()  # Sauvegarde de la base de données
# Menu d'options   fais avec copilot car plus rapide à écrire.
while True:
    print("\nOptions:")
    print("1. Ajouter un Livre")
    print("2. Retirer un Livre")
    print("3. Rechercher des Livres")
    print("4. Emprunter un Livre")
    print("5. Retourner un Livre")
    print("6. Ajouter un Utilisateur")
    print("7. Afficher Tous les Utilisateurs")
    print("8. Sauvegarder et Quitter")

    choix = input("Entrez votre choix (1-8): ")

    if choix == '1':
        titre = input("Entrez le titre du livre: ")
        auteur = input("Entrez l'auteur du livre: ")
        categorie = input("Entrez la catégorie du livre: ")
        nouveau_livre = Livre(titre, auteur, categorie)
        db.ajouter_livre(nouveau_livre)
        print(f"Livre '{titre}' ajouté à la bibliothèque.")
    elif choix == '2':
        titre = input("Entrez le titre du livre à retirer: ")
        livres_correspondants = [livre for livre in db.livres if titre.lower() in livre.titre.lower()]
        if livres_correspondants:
            livre_a_retirer = livres_correspondants[0]
            db.retirer_livre(livre_a_retirer)
            print(f"Livre '{titre}' retiré de la bibliothèque.")
        else:
            print(f"Livre '{titre}' non trouvé dans la bibliothèque.")
    elif choix == '3':
        terme_recherche = input("Entrez le terme de recherche: ")
        strategie_recherche = input("Choisissez la stratégie de recherche (titre/auteur/catégorie): ")
        if strategie_recherche.lower() == 'titre':
            strategie = StrategieRechercheTitre()
        elif strategie_recherche.lower() == 'auteur':
            strategie = StrategieRechercheAuteur()
        elif strategie_recherche.lower() == 'catégorie':
            strategie = StrategieRechercheCategorie()
        else:
            print("Stratégie de recherche invalide.")
            continue
        db.rechercher_livres(strategie, terme_recherche)
    elif choix == '4':
        nom_utilisateur = input("Entrez votre nom: ")
        titre_livre = input("Entrez le titre du livre à emprunter: ")
        utilisateur = next((u for u in db.utilisateurs if u.nom.lower() == nom_utilisateur.lower()), None)
        if utilisateur:
            livres_correspondants = [livre for livre in db.livres if titre_livre.lower() in livre.titre.lower()]
            if livres_correspondants:
                livre_a_emprunter = livres_correspondants[0]
                db.emprunter_livre(utilisateur, livre_a_emprunter)
            else:
                print(f"Livre '{titre_livre}' non trouvé dans la bibliothèque.")
        else:
            print(f"Utilisateur '{nom_utilisateur}' non trouvé.")
    elif choix == '5':
        nom_utilisateur = input("Entrez votre nom: ")
        titre_livre = input("Entrez le titre du livre à retourner: ")
        utilisateur = next((u for u in db.utilisateurs if u.nom.lower() == nom_utilisateur.lower()), None)
        if utilisateur:
            livres_correspondants = [livre for livre in db.livres if titre_livre.lower() in livre.titre.lower()]
            if livres_correspondants:
                livre_a_retourner = livres_correspondants[0]
                db.retourner_livre(utilisateur, livre_a_retourner)
            else:
                print(f"Livre '{titre_livre}' non trouvé dans la bibliothèque.")
        else:
            print(f"Utilisateur '{nom_utilisateur}' non trouvé.")
    elif choix == '6':
        nom_utilisateur = input("Entrez le nom du nouvel utilisateur: ")
        nouvel_utilisateur = Utilisateur(nom_utilisateur)
        db.ajouter_utilisateur(nouvel_utilisateur)
    elif choix == '7':
        db.afficher_tous_les_utilisateurs()
    elif choix == '8':
        db.sauvegarder_etat("bibliotheque.json")
        print("État de la bibliothèque sauvegardé. Sortie.")
        break
    else:
        print("Choix invalide. Veuillez entrer un nombre entre 1 et 8.")
