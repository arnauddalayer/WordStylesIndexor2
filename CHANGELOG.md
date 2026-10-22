# Changelog

## 2026-10-21

- CSV : toutes les valeurs texte sont maintenant entre guillemets, de façon uniforme (auparavant, seules les valeurs contenant une virgule, un guillemet ou un saut de ligne l'étaient). Le contenu lu par un tableur ou une bibliothèque CSV est identique.
- Ajout de la structure de tests unitaires (`tests/`, `tests/run_tests.bat`) et d'un test modèle (`tests/n/`), réutilisables pour d'autres « projets » : chaque sous-dossier est exécuté dans les deux formats et les deux ordres. `run_tests.bat` permet d'exécuter tous les tests (Entrée) ou un seul (numéro saisi ou passé en argument).

## 2026-10-20

- Ajout d'une sortie au format JSON (`--format json`, en plus du CSV) ; chaque entrée contient les mêmes champs que le CSV : `id`, `Fichier`, `Style`, `contenu`.
- Ajout de l'argument `--ordre` (`style` ou `document`) pour choisir l'ordre des entrées dans le rapport.
- Francisation du script : fonctions, variables et constantes en français (`parcourirRuns` devient `parcourirSegments`), et arguments en ligne de commande renommés : `--styles-file` → `--fichier-styles`, `--input-dir` → `--dossier-entree`, `--output-dir` → `--dossier-sortie` ; `--verbose` est conservé (aide `-h` / `--aide` en français).
- Les fichiers du dossier d'entrée sont traités en ordre alphabétique, pour un rapport reproductible.
- Le dossier de sortie n'est plus créé lorsque le dossier d'entrée n'existe pas.
- `requirements.txt` : version minimale de `python-docx` (1.2.0).
- `W_go.bat` : retrait d'une étiquette `:native` en double.
- Fichiers `.command` : droits d'exécution enregistrés dans Git.
- `.gitattributes` : fins de ligne CRLF forcées pour les `.bat`.
- `W_go.bat` et `W_install_requirements.bat` : l'avertissement « dossier temporaire » ne se déclenche plus que si un dossier nommé `temp` figure dans le chemin (et non plus pour tout chemin contenant « temp », ex. `Templates`).
- Licence MIT (remplace CC BY-NC-SA 2.5) ; l'historique est maintenant dans `CHANGELOG.md`, le README n'y renvoie que par un lien.

## 2026-09-28

- `W_go.bat` & `W_install_requirements.bat` : Protection contre l'exécution depuis un fichier ZIP non décompressé, et correction du chemin de travail lorsqu'exécuté en tant qu'administrateur.

## 2026-09-24

- `W_install_requirements.bat` : Amélioration de la détection de Miniforge

## 2026-09-21

- `W_install_requirements.bat` : Amélioration de la détection de Miniforge
- `_go` : Vérification que `.venv` n'est pas vide

## 2026-09-20

- Réécriture complète en Python, remplaçant le script VBS.
- Ajout de scripts d'installation et d'exécution multiplateformes (Windows `.bat`, macOS/Linux `.command`) avec détection automatique de Miniforge/Mamba/Conda.
- Sortie limitée à un fichier CSV (encodage `utf-8-sig` pour compatibilité Excel) ; la génération d'une base de données Access n'est plus offerte.
- La liste des styles à extraire est désormais définie dans `stylesAIndexer.txt` (un style par ligne) plutôt que codée en dur dans le script.
- Ajout d'arguments en ligne de commande (`--styles-file`, `--input-dir`, `--output-dir`, `--verbose`) pour surcharger la configuration par défaut.