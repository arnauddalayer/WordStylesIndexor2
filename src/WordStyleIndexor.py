import argparse
import docx
import csv
import os
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

# Valeurs par défaut, modifiables via les arguments en ligne de commande
# (utile notamment pour exécuter les tests unitaires du dossier tests/)
STYLES_FILE_DEFAUT = "stylesAIndexer.txt"
INPUT_DIR_DEFAUT = "docs"
OUTPUT_DIR_DEFAUT = "out"
# Style de caractère appliqué par défaut : ne pas le compter comme un "vrai" style
STYLE_CARACTERE_PAR_DEFAUT = "Default Paragraph Font"


def normaliserNomStyle(styleNom):
    # Les documents en anglais utilisent "Heading X" au lieu de "Titre X"
    return styleNom.replace("Heading", "Titre")


def parcourirParagraphes(document):
    # document.paragraphs ne renvoie que les paragraphes directement enfants du corps du document.
    # Un parcours récursif de l'arborescence XML est nécessaire pour aussi trouver les paragraphes
    # imbriqués dans les tableaux et les contrôles de contenu (ex. section répétitive).
    for p in document.element.body.iter(qn('w:p')):
        yield Paragraph(p, document)


def parcourirRuns(paragraphe):
    # paragraphe.runs ne renvoie que les <w:r> directement enfants du paragraphe. Un style de
    # caractère est souvent appliqué à un <w:r> imbriqué dans un contrôle de contenu (<w:sdt>)
    # placé à l'intérieur du paragraphe (ex. champ de saisie d'une section répétitive).
    for r in paragraphe._p.iter(qn('w:r')):
        yield Run(r, paragraphe)


def lireStylesAIndexer(cheminFichier):
    # Un style par ligne ; les lignes vides ou commençant par # sont ignorées
    if not os.path.exists(cheminFichier):
        print(f"Erreur : Le fichier de styles '{cheminFichier}' n'existe pas.")
        return []

    with open(cheminFichier, encoding='utf-8-sig') as f:
        return [ligne.strip() for ligne in f if ligne.strip() and not ligne.strip().startswith('#')]


def extraireStylesDesDocuments(stylesAIndexer, inputDir, outputDir, verbose=False):
    outputFile = os.path.join(outputDir, "rapport.csv")

    # S'assurer que le dossier de sortie existe
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        print(f"Création du dossier {outputDir}")

    # Utilisation de 'utf-8-sig' pour ajouter le BOM, ce qui permet à Excel
    # de reconnaître correctement l'encodage UTF-8 et d'afficher les accents.
    with open(outputFile, 'w', encoding='utf-8-sig', newline='') as csvfile:
        rapport = csv.writer(csvfile)
        # Écriture de l'en-tête
        rapport.writerow(["id", "Fichier", "Style", "contenu"])
        
        id_counter = 0        
        # Vérifier si le dossier source existe
        if not os.path.exists(inputDir):
            print(f"Erreur : Le dossier '{inputDir}' n'existe pas. Veuillez créer le dossier et y placer vos fichiers .docx")
            return

        print(f"Styles à extraire : {', '.join(stylesAIndexer)}")

        # Parcourir les fichiers du dossier spécifié
        for nomFichier in os.listdir(inputDir):
            # On ignore les fichiers temporaires de Word (commençant par ~$)
            if not (nomFichier.endswith('.docx') and not nomFichier.startswith('~$')):
                continue

            chemin = os.path.join(inputDir, nomFichier)
            print(f"Traitement du fichier {nomFichier}")

            try:
                docATraiter = docx.Document(chemin)
            except Exception as erreur:
                # Un fichier corrompu ou verrouillé ne doit pas interrompre le traitement des autres
                print(f"  [ERREUR] Impossible d'ouvrir {nomFichier} : {erreur}")
                continue

            # Paragraphes du document et des tableaux/contrôles de contenu qu'il contient
            tousLesParagraphes = list(parcourirParagraphes(docATraiter))

            # On récupère et on affiche les styles présents dans le document (toujours, en ordre alphabétique)
            # Les styles de paragraphe et les styles de caractère (appliqués sur des passages de texte) sont inclus.
            stylesParagraphe = (p.style.name for p in tousLesParagraphes)
            stylesCaractere = (r.style.name for p in tousLesParagraphes for r in parcourirRuns(p))
            stylesTrouves = sorted({s for s in list(stylesParagraphe) + list(stylesCaractere) if s != STYLE_CARACTERE_PAR_DEFAUT})
            print(f"  Styles détectés dans ce fichier : {', '.join(stylesTrouves)}")

            # Boucle par style recherché, puis par paragraphe : regroupe l'affichage
            # et le rapport par style (comme dans la version VBS)
            for styleNom in stylesAIndexer:
                if verbose:
                    # Affichage du style en cours dans la boucle des styles recherchés
                    print(f"    Recherche du style : {styleNom}")

                styleNomNormalise = normaliserNomStyle(styleNom)

                for para in tousLesParagraphes:
                    styleActuel = para.style.name

                    if normaliserNomStyle(styleActuel) == styleNomNormalise:
                        # Le style recherché est appliqué au paragraphe entier
                        extraction = para.text.strip()
                    else:
                        # Le style recherché peut aussi être un style de caractère, appliqué
                        # seulement à certains passages (runs) du paragraphe, y compris ceux
                        # imbriqués dans un contrôle de contenu
                        extraits = [r.text for r in parcourirRuns(para) if normaliserNomStyle(r.style.name) == styleNomNormalise]
                        extraction = ''.join(extraits).strip()

                    if extraction:
                        rapport.writerow([id_counter, nomFichier, styleNom, extraction])
                        id_counter += 1
                        if verbose:
                            # Affichage des 15 premiers caractères pour faciliter la vérification visuelle
                            preview = extraction[:15]
                            print(f"      Entrée ajoutée (Style: {styleActuel}) | Aperçu : {preview}...")

    print(f"Terminé. Le rapport est disponible dans : {outputFile}")


def analyserArguments():
    parser = argparse.ArgumentParser(description="Extrait le contenu des styles Word indiqués vers un fichier CSV.")
    parser.add_argument("--styles-file", default=STYLES_FILE_DEFAUT,
                         help=f"Fichier listant les styles à extraire, un par ligne (défaut : {STYLES_FILE_DEFAUT})")
    parser.add_argument("--input-dir", default=INPUT_DIR_DEFAUT,
                         help=f"Dossier contenant les fichiers .docx à traiter (défaut : {INPUT_DIR_DEFAUT})")
    parser.add_argument("--output-dir", default=OUTPUT_DIR_DEFAUT,
                         help=f"Dossier où écrire le rapport CSV (défaut : {OUTPUT_DIR_DEFAUT})")
    parser.add_argument("--verbose", action="store_true",
                         help="Active le mode détaillé pour le diagnostic")
    return parser.parse_args()


if __name__ == "__main__":
    args = analyserArguments()
    styles = lireStylesAIndexer(args.styles_file)
    if styles:
        extraireStylesDesDocuments(styles, args.input_dir, args.output_dir, args.verbose)
    print("Fin du traitement")