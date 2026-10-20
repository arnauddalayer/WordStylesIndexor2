# WordStylesIndexor2

Script pour l'extraction de données par les styles dans des documents Word

Ce projet est une réécriture en Python de l'outil original en VBS, disponible sur [github.com/arnauddalayer/WordStylesIndexor](https://github.com/arnauddalayer/WordStylesIndexor). La version Python fonctionne à la fois sous Windows et macOS/Linux.

# Présentation

WordStylesIndexor est un script que j'ai créé pour démontrer, dans le cadre du cours [INU1010 - Création de l'information numérique](https://cours.ebsi.umontreal.ca/planscours/inu1010), l'extraction de données depuis un document Word structuré à l'aide d'une feuille de style.

Plus précisément :
* Ce script extrait, à partir d'une collection de documents Word placés dans le dossier `docs`, les contenus structurés par styles.
* La liste des styles à indexer doit être spécifiée dans le fichier `stylesAIndexer.txt`, à raison d'un style par ligne (les lignes vides ou commençant par `#` sont ignorées).  
Par défaut, celui-ci va extraire les informations possédant les styles « Titre 1 » et « Titre 2 » (les équivalents anglais « Heading 1 »/« Heading 2 » sont également reconnus).
* Les contenus sont extraits vers un fichier de sortie (au choix, un fichier CSV ou un fichier JSON) qui contient : un identifiant, le nom du fichier, le nom du style et le contenu du paragraphe.
* Les styles recherchés peuvent être des styles de paragraphe (ex. « Titre 1 ») ou des styles de caractère appliqués sur une partie du texte (ex. un style appliqué au contenu d'un champ de formulaire ou d'une section répétitive) ; les deux types sont détectés, y compris lorsqu'ils sont imbriqués dans un tableau ou un contrôle de contenu.
* Le fichier de styles, ainsi que les dossiers d'entrée/sortie, peuvent être surchargés via des arguments en ligne de commande (`--fichier-styles`, `--dossier-entree`, `--dossier-sortie`, `--verbose`, `--ordre`, `--format`). Par exemple, l'argument `--ordre` permet de choisir entre un tri par style (`style`) ou par ordre d'apparition dans le document (`document`). `--aide` affiche la liste complète.

# Structure du projet

```
src/
├── docs/                           : déposez ici les fichiers .docx à indexer
├── out/                            : contiendra rapport.csv ou rapport.json, généré après l'exécution
├── stylesAIndexer.txt              : liste des styles à extraire (un par ligne)
├── WordStyleIndexor.py             : script principal
├── version.txt                     : date de la version
├── requirements.txt                : dépendances Python (python-docx)
├── W_install_requirements.bat      : installation des dépendances sous Windows
├── W_go.bat                        : exécution du script sous Windows
├── M_install_requirements.command  : installation des dépendances sous macOS/Linux
└── M_go.command                    : exécution du script sous macOS/Linux
tests/
├── run_tests.bat                   : exécute tous les tests unitaires (Windows)
└── <n>/                            : un dossier par test unitaire (voir tests/n/ pour un modèle)
    ├── stylesAIndexer.txt          : styles à extraire pour ce test
    ├── docs/                       : fichiers .docx utilisés par ce test
    ├── out/                        : rapports générés (un sous-dossier par ordre : style/ et document/)
    └── ref/                        : résultat de référence, pour comparaison manuelle
```

## Installation

### 1. Installer Python

Installez Python 3.10 ou plus récent (testé avec Python 3.14), ou utilisez un environnement Miniforge/Conda.

### 2. Installer les dépendances

Sous Windows :

```cmd
W_install_requirements.bat
```

Sous macOS/Linux :

```bash
./M_install_requirements.command
```

Ces scripts :

- créent un environnement virtuel `.venv`;
- installent les dépendances requises.

# Utilisation

* Placez les documents `.docx` à indexer dans le dossier `docs`.
* Au besoin, éditez `stylesAIndexer.txt` pour changer les styles recherchés (un style par ligne).
* Sous Windows, double-cliquez sur `W_go.bat`. Sous macOS/Linux, double-cliquez sur `M_go.command` (ou exécutez-le dans un terminal).
* Le script affiche la liste des styles recherchés, puis pour chaque document la liste des styles qu'il contient, ce qui facilite l'ajustement de `stylesAIndexer.txt`. Le rapport est généré dans `src/out/`.
* Le script accepte aussi des arguments en ligne de commande pour surcharger ces valeurs, par exemple :
  ```
  python WordStyleIndexor.py --fichier-styles autreStyles.txt --dossier-entree autresDocs --dossier-sortie autreSortie --verbose --ordre document --format json
  ```

## Formats de sortie

Dans les deux formats, chaque entrée contient les champs `id`, `Fichier`, `Style` et `contenu`.

* **CSV** (`rapport.csv`, défaut) : encodage `utf-8-sig`, pour une ouverture directe dans Excel.
* **JSON** (`rapport.json`) : encodage `utf-8`, tableau d'objets.

## Tests unitaires

Les tests permettent de vérifier le comportement du script sur vos propres documents. Pour en créer un, copiez `tests/n/` sous un nouveau nom, remplacez son contenu (`docs/` et `stylesAIndexer.txt`), puis exécutez `tests\run_tests.bat` (après avoir installé les dépendances). Chaque test est exécuté dans les deux formats et les deux ordres.

# Limitations

* Contrairement à la version VBS, cette version ne génère pas de base de données Access; seuls des fichiers CSV ou JSON sont produits.

# Licence et changelog

Ce projet est distribué sous licence MIT (voir [LICENSE](LICENSE)). L'historique des versions est dans [CHANGELOG.md](CHANGELOG.md).

# Utilisation de l'IAg

La création de ce projet a été réalisée avec l’IA (en local avec gemma4:12b via Ollama, et avec Github Copilot en mode auto).

<img alt="Réalisé avec l'IA" loading="lazy" src="https://d1qywhc7l90rsa.cloudfront.net/accounts/152505/images/Label-IA_fondclair.png" width="200" height="80">
