
#########################################################################
# Étape 1 : préparation de l'expérience 
#########################################################################
    #imports 
    #input arguments (sujet, session, condition)
    #creer nom fichier : nom_fichier = f'mini_exp_{sujet}.npy' 
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

#########################################################################
# Étape 3 : expérience (boucle principale) -> tache same-difference 
#########################################################################
#       1er boucle : image same -> générer aléatoirement paire d'images identique (np.random.random) pour 30% des essais 
#       2e boucle : image differente -> générer aléatoirement 2 images diff pour 70% des essais 
#       Si la condition = 1 -> présenter des images identiques 
#       Sinon --> présenter 2 images différentes (aléatoires)
#       dessiner la croix de fixation
#       Afficher les 2 images (visual.stim) + croix fixation 
#       Débute le chronomètre 
#       Attend qu'on appuie sur touche + arrête le chronomètre 
#       Calcul le temps de réponse 
#       Enregistre les réponses : Temps_de_reponses; reponses; index_image_gauche; index_image_droite; nom_image_gauche; nom_image_droite
# Boucle if : EXACTITUDE + FEEDBACK 
#       vérifier si la personne a appuyé sur la bonne touche 
#       si image same (condition 1) --> appuyer sur i + enregistrer rép ds résult (touche + tps rép)
#       si image differente (condition 0) --> appuyer sur d + enregistrer rép ds résult (touche + tps rép) 



#########################################################################
# Étape 1 : préparation de l'expérience 
#########################################################################
import sys
from psychopy import visual, event, core, monitors, gui
from datetime import datetime 
from PIL import Image
import numpy as np
import os
import random 
import pandas as pd 


# Input arguments 
sujet = str(sys.argv[0])
session = sys.argv[0]


# Créer une boîte de dialogue
dlg = gui.Dlg(title="Informations participant")
dlg.addField("Participant:", "")
dlg.addField("Session:", "")

# Vérifier si l'utilisateur a cliqué sur "OK"
if dlg.show() == gui.OK:
    # Récupérer les valeurs saisies par l'utilisateur
    numero_participant = dlg.data[0]
    numero_session = dlg.data[1]


# Création du fichier 
same_difference = f'exp_{sujet}_{session}.npy'

# Définir le chemin du fichier de progression pour le participant
fichier_progression = f'progression_{sujet}.txt'

# Vérifier si le fichier de progression existe
if os.path.isfile(fichier_progression):
    # Si le fichier existe, lire le numéro de l'essai en cours
    with open(fichier_progression, 'r') as f:
        essai_en_cours = int(f.read())
else:
    # Si le fichier n'existe pas, commencer à partir de l'essai 0
    essai_en_cours = 0



# Générer le seed 
np.random.seed()

# Dossier contenant les images
dossier_images = '/Users/ayaazbane/Desktop/AUT2023/Programmationneuro/travailFinal/banque_images'

# Charger la liste des fichiers d'images
liste_images = [f for f in os.listdir(dossier_images) if f.endswith('.png')]


#########################################################################
# Étape 2 : définir les variables de l'expérience 
#########################################################################
# Dictionnaire contenant les résultats
resultats = {'temps_de_reponse': [], 'reponses': [], 'index_image_gauche': [], 'index_image_droite': [], 'nom_image_gauche': [],
             'nom_image_droite': [], 'feedback': []}

# Nombre d'essais et de répétitions
nb_stimuli = 1000
nb_conditions = 1
nb_repetitions = 4
nb_essais = nb_stimuli * nb_conditions * nb_repetitions

# Ordre aléatoire des images 
np.random.shuffle(liste_images)

# Générer les conditions d'essai
quelles_conditions = np.zeros(nb_essais)

# Assigner 30% des essais comme paires identiques 
indices_identiques = np.random.choice(nb_essais, size=int(nb_essais * 0.3), replace=False)
quelles_conditions[indices_identiques] = 1  # Identiques

# Créer une fenêtre PsychoPy
win = visual.Window(size=(800, 600), monitor='testMonitor', units='pix', fullscr=False)

# Textes d'instructions de la tâche 
instruction_texte = visual.TextStim(win, text= "Indiquez si les deux images qui vous seront présentées sont identiques ou différentes en appuyant sur la touche 'I' si elles sont identiques et appuyez sur la touche 'D' si les 2 images sont différentes. Appuyer sur la touche 'Entrée' afin de débuter la tâche",
                                     pos=(0, 0), height=20, color='white')

# Affichage des instructions
instruction_texte.draw()
win.flip()

# Attendre que l'utilisateur appuie sur la touche entrée pour commencer
event.waitKeys(keyList=['return'])

# Réinitialiser la position des instructions pour les essais
instruction_texte.pos = (0, 220)

# Croix de fixation
vertical = visual.Line(win, start=(-10, 0), end=(10, 0), lineWidth=1, lineColor=[1,-1,-1], colorSpace='rgb') # ligne verticale de la croix 
horizontal = visual.Line(win, start=(0,-10), end=(0,10), lineWidth=1, lineColor=[1,-1,-1], colorSpace='rgb') # ligne horizontale de la croix 
fixation = (vertical, horizontal) 

# Créer une liste de paires d'images 
paires_images = []

# Sélectionner les paires d'images identiques 
for i in range(0, len(liste_images), 2):
    paire_identique = [liste_images[i], liste_images[i]]
    paires_images.append(paire_identique)

# Sélectionner les paires d'images différentes
for i in range(1, len(liste_images), 2):
    paire_different = [liste_images[i], liste_images[(i + 1) % len(liste_images)]]
    paires_images.append(paire_different)


#########################################################################
# Étape 3 : boucle principale de la tache same-difference 
#########################################################################

# Boucle d'essais aléatoires
for essai in range(essai_en_cours, nb_essais):
    # Sélection deux images selon l'ordre de paires_images
    index_image_gauche = essai * 2
    index_image_droite = (essai * 2 + 1) % len(paires_images)

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
    resultats['numéro_participant'].append()
    
    
    # enregistrement de la progression des participants
    with open(fichier_progression, 'w') as f:
        f.write(str(essai))

    # Sauvegardez le dictionnaire complet dans un fichier
    np.save(same_difference, resultats)

    # Vérification de la réponse et affichage de la rétroaction 
    if (quelles_conditions[essai] == 1 and touches[0]== 'i') or (quelles_conditions[essai] == 0 and touches[0] == 'd'):
        exacte = "Bonne réponse !"
        feedback_texte = visual.TextStim(win, text=exacte, pos=(0, -200), height=20, color='green')
        resultats['feedback'].append(exacte)

    else:
        non_exacte = "Mauvaise réponse !"
        feedback_texte = visual.TextStim(win, text=non_exacte, pos=(0, -200), height=20, color='red')
        resultats['feedback'].append(non_exacte)

    feedback_texte.draw()
    win.flip()
    core.wait(1)  # Affichage du feedback pendant 1 seconde
    
# Fermeture de la fenêtre PsychoPy
win.close()

#########################################################################
# Étape 4 : Affichage, sauvegarde et conversion des résultats
#########################################################################

print("Temps de réponse par essai:", resultats['temps_de_reponse'])
print("Réponses par essai:", resultats['reponses'])
print("Index image gauche par essai:", resultats['index_image_gauche'])
print("Index image droite par essai:", resultats['index_image_droite'])
print("Le nom de l'image de gauche:", resultats['nom_image_gauche'])
print("Le nom de l'image de droite:", resultats['nom_image_droite'])
print("Feedback par essai: ", resultats['feedback'])


# sauvegarde le dictionnaire resultats    
np.save(same_difference, resultats, allow_pickle=True)


# Enregistrer le dataframe en CSV et ajouter les resultats à la session précédente 
resultats_df = pd.DataFrame(resultats)
resultats_df.to_csv('resultats.csv', mode='a', index=False, header=not os.path.isfile('resultats.csv'))


# Vérification des assertions pour la rétroaction
if quelles_conditions[essai] == 1:  # Images identiques
    if touches[0] == 'i':
        assert feedback_texte.text == "Bonne reponse!", "Feedback incorrect pour une reponse correcte (images identiques)."
    elif touches[0] == 'd':
        assert feedback_texte.text == "Mauvaise reponse!", "Feedback incorrect pour une reponse incorrecte (images identiques)."
elif quelles_conditions[essai] == 0:  # Images différentes
    if touches[0] == 'i':
        assert feedback_texte.text == "Mauvaise reponse!", "Feedback incorrect pour une reponse incorrecte (images différentes)."
    elif touches[0] == 'd':
        assert feedback_texte.text == "Bonne reponse!", "Feedback incorrect pour une reponse correcte (images différentes)."





