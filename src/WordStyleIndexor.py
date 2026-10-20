import argparse
import docx
import csv
import os
import json
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.text.run import Run

# Valeurs par défaut, modifiables via les arguments en ligne de commande
# (utile notamment pour exécuter les tests unitaires du dossier tests/)
FICHIER_STYLES_DEFAUT = "stylesAIndexer.txt"
DOSSIER_ENTREE_DEFAUT = "docs"
DOSSIER_SORTIE_DEFAUT = "out"
# Format de sortie par défaut ('csv' ou 'json')
FORMAT_DEFAUT = "csv"
# Style de caractère appliqué par défaut : ne pas le compter comme un "vrai" style
STYLE_CARACTERE_PAR_DEFAUT = "Default Paragraph Font"
# Ordre par défaut des résultats dans le rapport ('style' ou 'document')
ORDRE_DEFAUT = 'style'

def normaliserNomStyle(styleNom):
    # Les documents en anglais utilisent "Heading X" au lieu de "Titre X"
    return styleNom.replace("Heading", "Titre")


def parcourirParagraphes(document):
    # document.paragraphs ne renvoie que les paragraphes directement enfants du corps du document.
    # Un parcours récursif de l'arborescence XML est nécessaire pour aussi trouver les paragraphes
    # imbriqués dans les tableaux et les contrôles de contenu (ex. section répétitive).
    for elementParagraphe in document.element.body.iter(qn('w:p')):
        yield Paragraph(elementParagraphe, document)


def parcourirSegments(paragraphe):
    # Un « segment » correspond à un <w:r> (Run dans python-docx).
    # paragraphe.runs ne renvoie que les <w:r> directement enfants du paragraphe. Un style de
    # caractère est souvent appliqué à un <w:r> imbriqué dans un contrôle de contenu (<w:sdt>)
    # placé à l'intérieur du paragraphe (ex. champ de saisie d'une section répétitive).
    for elementSegment in paragraphe._p.iter(qn('w:r')):
        yield Run(elementSegment, paragraphe)


def lireStylesAIndexer(cheminFichier):
    # Un style par ligne ; les lignes vides ou commençant par # sont ignorées
    if not os.path.exists(cheminFichier):
        print(f"[ERREUR] Le fichier de styles '{cheminFichier}' n'existe pas.")
        return []

    with open(cheminFichier, encoding='utf-8-sig') as fichier:
        return [ligne.strip() for ligne in fichier if ligne.strip() and not ligne.strip().startswith('#')]


def extraireStylesDesDocuments(stylesAIndexer, dossierEntree, dossierSortie, ordre=ORDRE_DEFAUT, verbose=False, formatSortie=FORMAT_DEFAUT):

    # Vérifier si le dossier source existe
    if not os.path.exists(dossierEntree):
        print(f"[ERREUR] Le dossier '{dossierEntree}' n'existe pas. Veuillez créer le dossier et y placer vos fichiers .docx")
        return

    # S'assurer que le dossier de sortie existe
    if not os.path.exists(dossierSortie):
        os.makedirs(dossierSortie)
        print(f"[INFO] Création du dossier {dossierSortie}")

    # Afficher la configuration actuelle
    print(f"[INFO] Styles à extraire : {', '.join(stylesAIndexer)}")
    print(f"[INFO] Ordre de tri sélectionné : {ordre}")
    print(f"[INFO] Format de sortie : {formatSortie}")

    # Liste de dictionnaires regroupant les données extraites de tous les fichiers (Fichier, Style, contenu)
    donneesCollectionFichiers = []
    
    # Parcourir les fichiers du dossier spécifié (triés pour obtenir un rapport reproductible)
    for nomFichier in sorted(os.listdir(dossierEntree)):
        # On ignore les fichiers temporaires de Word (commençant par ~$)
        if not (nomFichier.endswith('.docx') and not nomFichier.startswith('~$')):
            continue

        chemin = os.path.join(dossierEntree, nomFichier)
        print(f"[INFO] Traitement du fichier {nomFichier}")

        try:
            docATraiter = docx.Document(chemin)
        except Exception as erreur:
            # Un fichier corrompu ou verrouillé ne doit pas interrompre le traitement des autres
            print(f"[ERREUR] Impossible d'ouvrir {nomFichier} : {erreur}")
            continue

        # Paragraphes du document et des tableaux/contrôles de contenu qu'il contient
        tousLesParagraphes = list(parcourirParagraphes(docATraiter))

        # On récupère et on affiche les styles présents dans le document (toujours, en ordre alphabétique)
        # Les styles de paragraphe et les styles de caractère (appliqués sur des passages de texte) sont inclus.
        stylesParagraphe = (paragraphe.style.name for paragraphe in tousLesParagraphes)
        stylesCaractere = (segment.style.name for paragraphe in tousLesParagraphes for segment in parcourirSegments(paragraphe))
        stylesTrouves = sorted({style for style in list(stylesParagraphe) + list(stylesCaractere) if style != STYLE_CARACTERE_PAR_DEFAUT})
        print(f"[INFO]   Styles détectés dans ce fichier : {', '.join(stylesTrouves)}")
        
        # On parcourt le document une seule fois pour collecter les données
        donneesDuDocument = []
        stylesAExtraireNomNormalise = {normaliserNomStyle(style) for style in stylesAIndexer}
        for paragraphe in tousLesParagraphes:
            
            extraction = ""
            styleActuel = paragraphe.style.name
            styleActuelNomNormalise = normaliserNomStyle(styleActuel)

            # 1. Vérifier si le paragraphe lui-même a un style cible
            if styleActuelNomNormalise in stylesAExtraireNomNormalise:
                extraction = paragraphe.text.strip()

            # 2. Sinon, vérifier les styles de caractères
            if not extraction:
                for styleNom in stylesAIndexer:
                    styleNomNormalise = normaliserNomStyle(styleNom)
                    
                    extraction = ''.join(
                        segment.text
                        for segment in parcourirSegments(paragraphe)
                        if normaliserNomStyle(segment.style.name) == styleNomNormalise
                    ).strip()

                    # Sortir de la boucle for styleNom en cours dès qu'un style est trouvé
                    if extraction:
                        # Mise à jour de styleActuel pour refléter le style de caractère trouvé
                        styleActuel = styleNom
                        break

            if extraction:
                # On stocke le nom normalisé pour le rapport
                styleNomAffiche = normaliserNomStyle(styleActuel)
                donneesDuDocument.append({
                    "Fichier": nomFichier,
                    "Style": styleNomAffiche,
                    "contenu": extraction
                })
                if verbose:
                    # Affichage des 15 premiers caractères pour faciliter la vérification visuelle
                    apercu = extraction[:15]
                    print(f"[INFO]     Entrée ajoutée (Style: {styleNomAffiche}) | Aperçu : {apercu}...")


        # On trie par nom de style (alphabétique) si demandé par argument
        if ordre == 'style':
            donneesDuDocument.sort(key=lambda entree: entree['Style'])
        # On ajoute les données du document à la collection globale
        donneesCollectionFichiers.extend(donneesDuDocument)

    # Un identifiant séquentiel est attribué à chaque entrée, identique pour le CSV et le JSON
    entrees = [{"id": identifiant, **entree} for identifiant, entree in enumerate(donneesCollectionFichiers)]

    # Écriture du fichier final selon le format demandé
    cheminSortie = os.path.join(dossierSortie, "rapport." + formatSortie)

    if formatSortie == "csv":
        with open(cheminSortie, 'w', encoding='utf-8-sig', newline='') as fichierCsv:
            rapport = csv.writer(fichierCsv)
            rapport.writerow(["id", "Fichier", "Style", "contenu"])
            for entree in entrees:
                rapport.writerow([entree['id'], entree['Fichier'], entree['Style'], entree['contenu']])
    else:
        with open(cheminSortie, 'w', encoding='utf-8') as fichierJson:
            json.dump(entrees, fichierJson, indent=4, ensure_ascii=False)

    print(f"[INFO] Terminé. Le rapport est disponible dans : {cheminSortie}")


def analyserArguments():
    parser = argparse.ArgumentParser(description="Extrait le contenu des styles Word indiqués vers un fichier CSV ou JSON.", add_help=False)
    parser.add_argument("-h", "--aide", "--help", action="help", help="Affiche ce message d'aide et quitte")
    parser.add_argument("--fichier-styles", default=FICHIER_STYLES_DEFAUT,
                        help=f"Fichier listant les styles à extraire, un par ligne (défaut : {FICHIER_STYLES_DEFAUT})")
    parser.add_argument("--dossier-entree", default=DOSSIER_ENTREE_DEFAUT,
                        help=f"Dossier contenant les fichiers .docx à traiter (défaut : {DOSSIER_ENTREE_DEFAUT})")
    parser.add_argument("--dossier-sortie", default=DOSSIER_SORTIE_DEFAUT,
                        help=f"Dossier où écrire le rapport (défaut : {DOSSIER_SORTIE_DEFAUT})")
    parser.add_argument("--ordre", choices=['style', 'document'], default=ORDRE_DEFAUT,
                        help="Ordre des résultats dans le rapport : 'style' (groupés par type) ou 'document' (ordre d'apparition) "
                             f"(défaut : {ORDRE_DEFAUT})")
    parser.add_argument("--format", choices=['csv', 'json'], default=FORMAT_DEFAUT,
                        help=f"Format du fichier de sortie : 'csv' ou 'json' (défaut : {FORMAT_DEFAUT})")
    parser.add_argument("--verbose", action="store_true",
                        help="Active le mode détaillé pour le diagnostic")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = analyserArguments()
    styles = lireStylesAIndexer(arguments.fichier_styles)
    if styles:
        extraireStylesDesDocuments(styles, arguments.dossier_entree, arguments.dossier_sortie, arguments.ordre, arguments.verbose, arguments.format)
    print("[INFO] Fin du traitement")