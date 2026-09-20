# WordStylesIndexor

Script pour l'extraction de données par les styles dans des documents Word

# Présentation

WordStylesIndexor est un script que j'ai créé pour démontrer, dans le cadre du cours [INU1010 - Création de l'information numérique](https://cours.ebsi.umontreal.ca/planscours/inu1010), l'extraction de données depuis un document Word structuré à l'aide d'une feuille de style.

Plus précisément :
* Ce script extrait, à partir d'une collection de documents Word placés dans le dossier `docs`, les contenus structurés par styles.
* La liste des styles à indexer doit être spécifiée dans le fichier `stylesAIndexer.txt`, à raison d'un style par ligne (les lignes vides ou commençant par `#` sont ignorées).  
Par défaut, celui-ci va extraire les informations possédant les styles « Titre 1 » et « Titre 2 » (les équivalents anglais « Heading 1 »/« Heading 2 » sont également reconnus).
* Les contenus sont extraits vers un fichier CSV (`out/rapport.csv`) qui contient : un identifiant, le nom du fichier, le nom du style et le contenu du paragraphe.
* Les styles recherchés peuvent être des styles de paragraphe (ex. « Titre 1 ») ou des styles de caractère appliqués sur une partie du texte (ex. un style appliqué au contenu d'un champ de formulaire ou d'une section répétitive) ; les deux types sont détectés, y compris lorsqu'ils sont imbriqués dans un tableau ou un contrôle de contenu.
* Le fichier de styles, ainsi que les dossiers d'entrée/sortie, peuvent être surchargés via des arguments en ligne de commande (`--styles-file`, `--input-dir`, `--output-dir`, `--verbose`), ce qui permet notamment d'exécuter les tests unitaires du dossier `tests/`.

Ce projet est une réécriture en Python de l'outil original en VBS, disponible sur [github.com/arnauddalayer/WordStylesIndexor](https://github.com/arnauddalayer/WordStylesIndexor). La version Python fonctionne à la fois sous Windows et macOS/Linux.

# Structure du projet

```
src/
├── docs/                          : déposez ici les fichiers .docx à indexer
├── out/                           : contiendra rapport.csv, généré après l'exécution
├── stylesAIndexer.txt             : liste des styles à extraire (un par ligne)
├── WordStyleIndexor.py            : script principal
├── requirements.txt                : dépendances Python (python-docx)
├── W_install_requirements.bat      : installation des dépendances sous Windows
├── W_go.bat                        : exécution du script sous Windows
├── M_install_requirements.command  : installation des dépendances sous macOS/Linux
├── M_go.command                   : exécution du script sous macOS/Linux
tests/
├── run_tests.bat                  : exécute tous les tests unitaires (Windows)
└── <n>/                           : un dossier par test unitaire
    ├── stylesAIndexer.txt         : styles à extraire pour ce test
    ├── docs/                      : fichiers .docx utilisés par ce test
    ├── out/                       : rapport.csv généré par ce test
    └── ref/                       : résultat de référence, pour comparaison manuelle
```

# Installation

* [Installez Python 3](https://www.python.org/downloads/) si ce n'est pas déjà fait (ou un environnement Miniforge/Conda, qui est automatiquement détecté).
* Sous Windows, double-cliquez sur `W_install_requirements.bat`.
* Sous macOS/Linux, rendez les fichiers `.command` exécutables avec `chmod +x *.command` et double-cliquez ensuite sur `M_install_requirements.command` (ou exécutez-le dans un terminal).

Ces scripts créent un environnement virtuel (`.venv`) et y installent les dépendances listées dans `requirements.txt`.

# Utilisation

* Placez les documents `.docx` à indexer dans le dossier `docs`.
* Au besoin, éditez `stylesAIndexer.txt` pour changer les styles recherchés (un style par ligne).
* Sous Windows, double-cliquez sur `W_go.bat`. Sous macOS/Linux, double-cliquez sur `M_go.command` (ou exécutez-le dans un terminal).
* Le script affiche la liste des styles recherchés, puis pour chaque document la liste des styles qu'il contient, ce qui facilite l'ajustement de `stylesAIndexer.txt`. Le rapport est généré dans `src/out/rapport.csv`.
* Le script accepte aussi des arguments en ligne de commande pour surcharger ces valeurs, par exemple :
  ```
  python WordStyleIndexor.py --styles-file autreStyles.txt --input-dir autresDocs --output-dir autreSortie --verbose
  ```

# Limitations

* Contrairement à la version VBS, cette version ne génère pas de base de données Access; seul un fichier CSV est produit.

# Licence

Cette création est mise à disposition selon le Contrat Paternité-NonCommercial-ShareAlike2.5 Canada disponible en ligne http://creativecommons.org/licenses/by-nc-sa/2.5/ca/ ou par courrier postal à Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.

# Changelog

**2026-09-20**
* Réécriture complète en Python (`WordStyleIndexor.py`), remplaçant le script VBS.
* Ajout de scripts d'installation et d'exécution multiplateformes (Windows `.bat`, macOS/Linux `.command`) avec détection automatique de Miniforge/Mamba/Conda.
* Sortie limitée à un fichier CSV (encodage `utf-8-sig` pour compatibilité Excel) ; la génération de base Access est retirée.
* La liste des styles à extraire est désormais définie dans `stylesAIndexer.txt` (un style par ligne) plutôt que codée en dur dans le script.
* Ajout d'arguments en ligne de commande (`--styles-file`, `--input-dir`, `--output-dir`, `--verbose`) pour surcharger la configuration.

## Utilisation de l'IAg

La réécriture en Python (code et documentation) a été réalisée avec l’IA (en local avec gemma4:12b via Ollama, et avec Github Copilot en mode auto).

<img alt="Réalisé avec l'IA" loading="lazy" src="https://d1qywhc7l90rsa.cloudfront.net/accounts/152505/images/Label-IA_fondclair.png" style="width: 200px; height: 80px;">
