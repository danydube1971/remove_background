Remove Background 1.7 - Guide d'utilisation
===========================================

Remove Background 1.7 est une application graphique Python qui permet de supprimer l'arrière-plan d'une image et de sauvegarder le résultat au format PNG (raster) ou SVG (vectoriel). Elle utilise rembg pour la suppression du fond et potrace pour la vectorisation en SVG.

![Remove_background](https://github.com/user-attachments/assets/d03fdb4a-71ed-4f5c-ab76-b9a87bba357e)


Fonctionnalités
---------------

-   **Interface graphique** : Sélectionnez une image, choisissez un format de sortie, et prévisualisez le résultat.

-   **Formats de sortie** :

    -   **PNG** : Image raster avec transparence et opacité ajustable via un slider.

    -   **SVG** : Fichier vectoriel avec contours noirs basé sur les bords de l'objet.

-   **Modèles personnalisables** : Choisissez parmi différents modèles rembg (u2netp, u2net, etc.).

-   **Prévisualisation** : Voir l'image originale et le résultat côte à côte.

Prérequis
---------

Avant d'exécuter le script, assurez-vous d'installer les dépendances nécessaires. Voici les étapes détaillées, avec une attention particulière à potrace pour éviter les problèmes rencontrés lors de la mise en place.

### Dépendances système (Linux)

Ces commandes sont pour Ubuntu/Debian/Linux Mint. Adaptez-les selon votre distribution.

1.  **Mettre à jour le système** :

    `sudo apt-get update`

2.  **Installer les outils de compilation et dépendances de développement** :

    `sudo apt-get install build-essential python3-dev pkg-config`

1.  **Installer potrace** :

    `sudo apt-get install potrace libpotrace-dev`

    -   potrace est l'outil de vectorisation principal.

    -   libpotrace-dev fournit les fichiers de développement nécessaires pour pypotrace.

2.  **Installer libagg-dev** (essentiel pour pypotrace) :

    `sudo apt-get install libagg-dev`

    -   Sans cette bibliothèque, l'installation de pypotrace échouera avec une erreur comme Package 'libagg' not found.

3.  **Vérifier l'installation de libagg** :

    `pkg-config --modversion libagg`

    -   Si une version s'affiche (ex. 2.5), tout est correct. Sinon, vérifiez que libagg.pc est dans /usr/lib/x86_64-linux-gnu/pkgconfig avec :

        `ls /usr/lib/x86_64-linux-gnu/pkgconfig/libagg.pc`\
        Si absent, réinstallez libagg-dev ou ajustez PKG_CONFIG_PATH :

        `export`` PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig:``$PKG_CONFIG_PATH`

### Dépendances Python

Utilisez Python 3.8+ (testé avec 3.12). Créez un environnement virtuel si souhaité :

`python3 -m venv venv`

`source venv/bin/activate`

Installez les bibliothèques Python :

`pip install numpy pillow pyqt5 rembg pypotrace`

-   numpy : Pour manipuler les tableaux d'images.

-   pillow : Pour traiter les images.

-   pyqt5 : Pour l'interface graphique.

-   rembg : Pour supprimer l'arrière-plan.

-   pypotrace : Interface Python pour potrace. Si l'installation échoue, assurez-vous que libagg-dev et libpotrace-dev sont bien présents (voir ci-dessus).

### macOS

-   Installez potrace via Homebrew :

    `brew install potrace`

-   Installez les dépendances Python avec pip comme ci-dessus. Si pypotrace échoue, ajoutez libagg manuellement (Homebrew ne fournit pas toujours libagg par défaut).

### Windows

-   Téléchargez potrace depuis [le site officiel](http://potrace.sourceforge.net/) et ajoutez-le au PATH.

-   Installez les dépendances Python avec pip dans un environnement virtuel. pypotrace peut nécessiter un compilateur (ex. Visual Studio Build Tools).

Installation
------------

2.  **Lancez le script** :

    `python3 remove_background_1.7.py`

Utilisation
-----------

1.  **Lancer l'application** : Une fenêtre s'ouvre avec le titre "Remove background 1.2".

2.  **Sélectionner une image** :

    -   Cliquez sur **"Sélectionner un fichier image"**.

    -   Choisissez une image (JPG, JPEG, PNG).

    -   Sélectionnez un dossier de sortie.

3.  **Configurer les options** :

    -   **Modèle** : Choisissez un modèle rembg dans la liste déroulante (ex. u2netp par défaut).

    -   **Opacité du fond** : Ajustez le slider (0 = transparent, 255 = opaque). Affecte le PNG et la prévisualisation.

    -   **Format de sortie** : Sélectionnez PNG (raster) ou SVG (vectoriel).

4.  **Supprimer le fond** :

    -   Cliquez sur **"Supprimer le fond"**.

    -   Une fois terminé, un message confirme la sauvegarde, et la prévisualisation s'affiche à droite (l'original est à gauche).

5.  **Vérifier le résultat** :

    -   **PNG** : Ouvre le fichier dans visionneuse d'images pour voir la transparence.

    -   **SVG** : Ouvre-le dans un éditeur comme Inkscape pour voir les contours vectoriels (noir sur fond transparent).

Remarques
---------

-   **SVG** : Les contours sont en noir, basés sur le canal alpha. Les couleurs originales ne sont pas conservées (vectorisation binaire).

-   **Prévisualisation** : Pour SVG, un PNG temporaire est généré pour l'affichage, car PyQt5 ne supporte pas les SVG nativement.

Dépannage
---------

-   **Erreur "Package 'libagg' not found"** :

    -   Installez libagg-dev (voir Prérequis).

-   **Erreur "ModuleNotFoundError: No module named 'potrace'"** :

    -   Vérifiez que pypotrace est installé avec pip install pypotrace.

-   **Erreur lors de la vectorisation** :

    -   Assurez-vous que potrace est dans votre PATH (which potrace sur Linux devrait retourner un chemin).
