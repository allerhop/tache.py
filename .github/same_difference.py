#########################################################################
# Étape 1 : préparation de l'expérience 
#########################################################################
    #imports 
    #input arguments (sujet, session, condition)
    #creer nom fichier : nom_fichier = f'mini_exp_{sujet}.npy' 
    #seed 
    #Charger la liste des fichiers d'images avec (banque d'images) 

#########################################################################
# Étape 2 : définir variables de l'expérience 
#########################################################################
#   nb_stimuli = 1000 
#   nb_conditions = 1   (1 : image same et 0: image differente)
#   nb_repetitions = 4
#   nb_d'essais = nb_repetition * nb_stimuli * nb_conditions
#   Création dictionnaire résultat : {'temps_de_reponse': [], 'reponses': [], 'index_image_gauche': [], 
#                                     'index_image_droite': [], 'nom_image_gauche': [],'nom_image_droite': [], 'feedback': []}

#   création VI (sans remise) + sauvegarder dans dictionnaire résultats 
#   création VD : 
#          reponses (matrice qui aura les touches appuyées par pers),
#          temps_de_reponse (contient les temps de réponses pour chaque essai)
#          nb_bonnes_rep (matrice de bonnes réponses)
#          nb_mauvaises_rep (matrice de mauvaises réponses)
#          index_image_gauche 
#          index_image_droite 
#          ajouter VD ds dictionnaire resultats 
#   créer une fenêtre : 
#          touches_de_reponses (matrice avec tt les touches possibles d'utiliser) 
#   créer une croix de fixation
#   créer une liste de paires d'images 
#Boucle qui génère 

#########################################################################
# Étape 3 : expérience (boucle principale) -> tache same-difference 
#########################################################################
#       1er boucle : image same -> générer aléatoirement paire d'images identique (np.random.random) pour 30% des essais + save dans seed !
#       2e boucle : image differente -> générer aléatoirement 2 images diff pour 70% des essais + save dans seed !
#       Si la condition = 1 -> présenter des images identiques 
#       Sinon --> présenter 2 images différentes (aléatoires)
#       dessiner la croix de fixation
#       Afficher les 2 images (visual.stim) + croix fixation 
#       Débute le chronomètre 
#       Attend qu'on appuie sur touche + arrête le chronomètre 
#       Calcul le temps de réponse 
#       Enregistre les réponses : Temps_de_reponses; reponses; index_image_gauche; index_image_droite; nom_image_gauche; nom_image_droite

# Boucle while? (tant que la pers a pas appuyer sur une touche, peut pas passer au prochain essai/stimulus) : EXACTITUDE + FEEDBACK 
#       vérifier si la personne a appuyé sur la bonne touche 
#       si image same (condition 1) --> appuyer sur i + enregistrer rép ds résult (touche + tps rép)
#       si image differente (condition 0) --> appuyer sur d + enregistrer rép ds résult (touche + tps rép) 




#########################################################################
# Étape 1 : préparation de l'expérience 
#########################################################################
from psychopy import visual, event, core, monitors
from datetime import datetime 
from PIL import Image
import numpy as np
import os
import random 

# Input arguments 
#sujet = str(sys.argv[1])
#session = sys.argv[2]
#condition = str(sys.argv[3])

# Création du fichier et vérification de l'existance du fichier 
#same_difference = f'exp_{sujet}_{session}_{condition}.npy'

#if os.path.isfile(same_difference):
#    print(f'\n\nLe fichier \"{same_difference}\" existe déjà.\n')
#    quit()

# Seeder le générateur de nombres pseudo-aléatoires
#np.random.seed()

# Dossier contenant les images
dossier_images = '/Users/ayaazbane/Desktop/AUT2023/Programmationneuro/travailFinal/banque_images'

# Charger la liste des fichiers d'images
liste_images = [f for f in os.listdir(dossier_images) if f.endswith('.png')]

#########################################################################
# Étape 2 : définir variables de l'expérience 
#########################################################################
# Dictionnaire pour stocker les résultats
resultats = {'temps_de_reponse': [], 'reponses': [], 'index_image_gauche': [], 'index_image_droite': [], 'nom_image_gauche': [],'nom_image_droite': [], 'feedback': []}

# Nombre d'essais et de répétitions
nb_stimuli = 1000
nb_conditions = 1
nb_repetitions = 4
nb_essais = nb_stimuli * nb_conditions * nb_repetitions

# Générer les conditions d'essai
quelles_conditions = np.zeros(nb_essais)

# Générer les conditions d'essai
quelles_conditions = np.zeros(nb_essais)

# Assigner 30% comme paires identiques et 70% comme paires différentes
indices_identiques = np.random.choice(nb_essais, size=int(nb_essais * 0.3), replace=False)
quelles_conditions[indices_identiques] = 1  # Identiques

# Répéter pour chaque condition
quelles_conditions = np.tile(quelles_conditions, nb_repetitions)

# Combiner les deux matrices
quels_stimuli_combined = np.concatenate((quelles_conditions, 1 - quelles_conditions))

# Mélanger les stimuli combinés de manière aléatoire
np.random.shuffle(quels_stimuli_combined)

# Créer une fenêtre PsychoPy
win = visual.Window(size=(800, 600), monitor='testMonitor', units='pix', fullscr=False)

# Textes d'instructions de la tâche 
instruction_texte = visual.TextStim(win, text= "Les deux images sont-elles identiques ou différentes ? Appuyez sur la touche 'I' si les 2 images sont identiques et appuyez sur la touche 'D' si les 2 images sont différentes. Appuyer sur enter pour débuter la tâche",
                                     pos=(0, 0), height=20, color='white')

# Afficher les instructions
instruction_texte.draw()
win.flip()

# Attendre que l'utilisateur appuie sur la touche Enter pour commencer
event.waitKeys(keyList=['return'])

# Réinitialiser la position des instructions pour les essais
instruction_texte.pos = (0, 220)

# Croix de fixation
vertical = visual.Line(win, start=(-10, 0), end=(10, 0), lineWidth=1, lineColor=[1,-1,-1], colorSpace='rgb') # ligne verticale de la croix 
horizontal = visual.Line(win, start=(0,-10), end=(0,10), lineWidth=1, lineColor=[1,-1,-1], colorSpace='rgb') # ligne horizontale de la croix 
fixation = (vertical, horizontal) 

# Créer une liste de paires d'images 
paires_images = []

#########################################################################
# Étape 3 : expérience (boucle principale) -> tache same-difference 
#########################################################################
# Boucle d'essais aléatoires
for essai in range(nb_essais):

    # Ajouter 30% de paires identiques
    for i in range(0, len(liste_images), 2):
        paire_identique = [liste_images[i], liste_images[i]]
        paires_images.append(paire_identique)

    # Ajouter 70% de paires différentes
    for i in range(1, len(liste_images), 2):
        paire_different = [liste_images[i], liste_images[(i + 1) % len(liste_images)]]
        paires_images.append(paire_different)

    # Sélection aléatoire de deux images
    index_image_gauche, index_image_droite = np.random.choice(len(paires_images), size=2, replace=False)

    # Si les images doivent être identiques
    if quelles_conditions[essai] == 1:
        image_gauche, image_droite = paires_images[index_image_gauche][0], paires_images[index_image_gauche][1]
    else:
        # Utiliser deux indices différents pour les images différentes
        index_image_droite = np.random.choice(np.setdiff1d(np.arange(len(paires_images)), index_image_gauche))
        image_gauche, image_droite = paires_images[index_image_gauche][0], paires_images[index_image_droite][1]

    # Affichage des images
    image_gauche_stim = visual.ImageStim(win, image=os.path.join(dossier_images, image_gauche), pos=(-170, 0),size=(250, 250))
    image_droite_stim = visual.ImageStim(win, image=os.path.join(dossier_images, image_droite), pos=(170, 0), size=(250, 250))


   # Affichage de la croix de fixation 
    for a_line in fixation:
        a_line.draw()

    image_gauche_stim.draw()
    image_droite_stim.draw()
    instruction_texte.draw()
    win.flip()

    # Enregistrement du temps de début
    temps_debut = core.getTime()

    # Attente de la réponse du participant
    touches = event.waitKeys(keyList=['i', 'd', 'escape'])

    # Enregistrement du temps de fin
    temps_fin = core.getTime()

    # Si la touche 'escape' est pressée, quitter l'expérience
    if 'escape' in touches:
        break

    # Calcul du temps de réponse
    temps_reponse = temps_fin - temps_debut

    # Enregistrement des réponses dans le dictionnaire de résultats
    resultats['temps_de_reponse'].append(temps_reponse)
    resultats['reponses'].append(touches[0])
    resultats['index_image_gauche'].append(index_image_gauche)
    resultats['index_image_droite'].append(index_image_droite)
    resultats['nom_image_gauche'].append(image_gauche)
    resultats['nom_image_droite'].append(image_droite)


    # Vérification de la réponse + affichage de la rétroaction 
    if (quelles_conditions[essai] == 1 and touches[0]== 'i') or (quelles_conditions[essai] == 0 and touches[0] == 'd'):
        feedback_texte = visual.TextStim(win, text="Bonne réponse!", pos=(0, -200), height=20, color='green')
        resultats['feedback'].append(feedback_texte)
    else:
        feedback_texte = visual.TextStim(win, text="Mauvaise réponse!", pos=(0, -200), height=20, color='red')
        resultats['feedback'].append(feedback_texte)

    feedback_texte.draw()
    win.flip()
    core.wait(1)  # Affichage du feedback pendant 1 seconde

# Fermeture de la fenêtre PsychoPy
win.close()

# Affichage des résultats
print("Temps de réponse par essai:", resultats['temps_de_reponse'])
print("Réponses par essai:", resultats['reponses'])
print("Index image gauche par essai:", resultats['index_image_gauche'])
print("Index image droite par essai:", resultats['index_image_droite'])
print("Le nom de l'image de gauche:", resultats['nom_image_gauche'])
print("Le nom de l'image de droite:", resultats['nom_image_droite'])


# Assertions --> ajouter des assertions pour le feedback selon si la personne répond correctement ou pas 
#assert nb_essais == len(quelles_conditions) == len(resultats['temps_de_reponse']) == len(resultats['reponses']) == len(resultats['index_image_gauche']) == len(resultats['index_image_droite']), "Les longueurs des listes ne correspondent pas."
#assert 0 <= index_image_gauche < len(paires_images), "Index_image_gauche hors de portée."
#assert 0 <= index_image_droite < len(paires_images), "Index_image_droite hors de portée."
#assert len(resultats['temps_de_reponse']) == len(resultats['reponses']) == len(resultats['index_image_gauche']) == len(resultats['index_image_droite']) == nb_essais, "Les longueurs des listes de résultats ne correspondent pas au nombre d'essais."


# Vérification des assertions pour la rétroaction
if quelles_conditions[essai] == 1:  # Images identiques
    if touches[0] == 'i':
        assert feedback_texte.text == "Bonne réponse!", "Feedback incorrect pour une réponse correcte (images identiques)."
    elif touches[0] == 'd':
        assert feedback_texte.text == "Mauvaise réponse!", "Feedback incorrect pour une réponse incorrecte (images identiques)."
elif quelles_conditions[essai] == 0:  # Images différentes
    if touches[0] == 'i':
        assert feedback_texte.text == "Mauvaise réponse!", "Feedback incorrect pour une réponse incorrecte (images différentes)."
    elif touches[0] == 'd':
        assert feedback_texte.text == "Bonne réponse!", "Feedback incorrect pour une réponse correcte (images différentes)."
