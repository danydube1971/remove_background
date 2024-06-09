# remove_background
Permet de faire du détourage dans une image automatiquement

Le script "Remove Background" permet de supprimer facilement le fond des images à l'aide d'un modèle d'intelligence artificielle. Il utilise une interface graphique conviviale qui vous guide tout au long du processus. Vous pouvez sélectionner une image, choisir un dossier de sortie, et supprimer le fond de l'image en quelques clics.

![Remove background](https://github.com/danydube1971/remove_background/assets/74633244/b95006a2-c0b2-4c94-b00d-618348ed8634)

### Testé dans Linux Mint 21.3 sous Python 3.11

## 1. Prérequis
 
   • Système d'exploitation : Linux, Windows, ou macOS.
   
   • Python : Version 3.6 ou supérieure.
   
   • Dépendances :
        ◦ PyQt5
        ◦ PIL (Pillow)
        ◦ rembg
   
## 2. Installation des Prérequis
Avant d'utiliser le script, assurez-vous que toutes les dépendances sont installées.

Installation de PyQt5
`pip install PyQt5 pillow rembg`

## 4. Lancement du Script
Pour exécuter le script, ouvrez un terminal et naviguez jusqu'au répertoire où le script est enregistré. 
Exécutez la commande suivante :

`python Remove_background.py`


## 5. Instructions d'Utilisation
   
### 5.1. Sélectionner une Image

   1. Cliquez sur le bouton "Sélectionner un fichier image".
   2. Une boîte de dialogue s'ouvre pour vous permettre de choisir une image sur votre ordinateur. Les formats pris en charge sont .jpg, .jpeg, et .png.
   3. Après avoir sélectionné l'image, choisissez un dossier de sortie pour enregistrer l'image modifiée.
   4. L'image sélectionnée s'affiche dans la zone de prévisualisation.
         
### 5.2. Supprimer le Fond de l'Image

   1. Cliquez sur le bouton "Supprimer le fond".
   2. Le script utilise le modèle de suppression de fond pour traiter l'image.
   3. Une fois le traitement terminé, une boîte de dialogue vous informe que l'image modifiée a été enregistrée dans le dossier de sortie spécifié.
   4. L'image sans fond s'affiche dans la zone de prévisualisation.
    
## 6. Gestion des Erreurs
   
Le script gère plusieurs erreurs courantes et affiche des messages pour vous aider à résoudre les problèmes :

   • Erreur d'Ouverture d'Image : Si l'image sélectionnée n'est pas valide ou ne peut pas être ouverte, un message d'erreur s'affiche.
   
   • Erreur de Sélection de Fichier : Si aucun fichier valide n'est sélectionné, un message d'erreur vous demande de sélectionner une image valide.
   
   • Erreur lors de la Suppression du Fond : Si une erreur survient lors de la suppression du fond, un message d'erreur s'affiche avec les détails de l'erreur.
   
## 7. Configuration du Modèle
Par défaut, le script utilise le modèle u2netp pour la suppression de fond. Vous pouvez changer le modèle en modifiant la ligne suivante dans le script :

`self.session = new_session('u2netp')`


Remplacez 'u2netp' par le modèle de votre choix, par exemple 'u2net' ou 'deeplabv3'.

## 8. Personnalisation de l'Interface
   
Vous pouvez personnaliser l'apparence de l'interface en modifiant les styles des boutons et la couleur de fond dans la méthode init_ui. 

Par exemple :

```self.setStyleSheet("background-color: #f0f0f0;")  # Couleur de fond
self.select_button.setStyleSheet("""
    QPushButton {
        background-color: #87ceeb;
        color: #ffffff;
        padding: 10px;
        border: none;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #00bfff;
    }
""")
```


## Les modèles disponibles pour « rembg » version 2.0.57 sont les suivants :

u2net  : Un modèle pré-entraîné pour les cas d'utilisation généraux.

u2netp  : Une version allégée du modèle u2net.

u2net_human_seg  : Un modèle pré-entraîné pour la segmentation humaine.

u2net_cloth_seg  : Un modèle pré-entraîné pour l'analyse des vêtements à partir d'un portrait humain. Ici, les vêtements sont classés en 3 catégories : Haut du corps, bas du corps et corps entier.

silueta  : Identique à u2net mais la taille est réduite à 43Mb.

isnet-general-use  : Un nouveau modèle pré-entraîné pour les cas d'utilisation générale.

isnet-anime : Une segmentation de haute précision pour les personnages d'anime.

sam : Un modèle pré-entraîné pour tous les cas d'utilisation.


