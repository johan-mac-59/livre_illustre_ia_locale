"""Contrôles d'images par un modèle à vision : scène et cohérence d'ensemble.

Le modèle répond à une grille de défauts (booléens true = défaut). C'est le code
qui décide : l'image est acceptée si aucun défaut n'est signalé. Les contrôles
s'appuient sur les fiches visuelles (personnages, animaux, lieux, éléments imposés).
"""
import fiches as modele_fiches
from llm import CONFIG, appeler_json, lire

DEFAUTS_SCENE = ("personnage_manquant", "personne_en_trop", "texte_visible",
                 "trait_non_conforme", "action_ou_decor_incorrect",
                 "element_impose_absent", "element_incongru", "deformation")
DEFAUTS_COHERENCE = ("visage_ou_cheveux_different", "age_ou_silhouette_different",
                     "vetements_differents", "decor_ou_objet_recurrent_different", "style_different")


def _decider(d, defauts):
    """Le code décide : ok si aucun défaut n'est à true."""
    signales = [nom for nom in defauts if d.get(nom) is True]
    ecarts = d.get("ecarts", [])
    if not isinstance(ecarts, list):
        ecarts = [str(ecarts)]
    return {"ok": not signales, "defauts": signales, "ecarts": [str(e) for e in ecarts],
            "correction_prompt": str(d.get("correction_prompt", "")) if signales else ""}


def controle_scene(image, illustration, fiches, journal, etiquette):
    """L'image respecte-t-elle la description, les fiches et les éléments imposés ?"""
    texte_fiches, imposes = modele_fiches.texte_controle(illustration, fiches)
    contenu = (f"## Illustration attendue\n{illustration['description']}\n\n"
               f"## Fiches à respecter\n{texte_fiches}\n\n"
               f"## Éléments imposés (doivent être visibles)\n{imposes}")
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_scene.md"), contenu,
                     cles=DEFAUTS_SCENE, images=[image], journal=journal, etiquette=etiquette)
    return _decider(d, DEFAUTS_SCENE)


def _description(fiches, ident):
    e = fiches["personnages"][ident]
    return f"{e.get('nom', ident)} ({modele_fiches.lignes(e)[0]})"


def controle_taille(image, illustration, fiches, journal, etiquette):
    """Le plus petit personnage est-il bien plus petit que le plus grand (sommet de la tête) ?

    Question étroite posée à un modèle à vision ; c'est le code qui compare à la relation
    attendue dans les fiches. Retourne None s'il n'y a aucune paire à contrôler.
    """
    paires = modele_fiches.tailles_a_controler(illustration, fiches)
    if not paires:
        return None
    ecarts, corrections = [], []
    for k, t in enumerate(paires, 1):
        contenu = (f"Personnage A : {_description(fiches, t['plus_petit'])}\n"
                   f"Personnage B : {_description(fiches, t['plus_grand'])}")
        d = appeler_json(CONFIG["roles"]["controleur_precis"], lire("agents/prompt_controleur_taille.md"),
                         contenu, cles=("tete_la_plus_haute", "ecart"), images=[image],
                         journal=journal, etiquette=f"{etiquette}_{k}")
        # B = le plus grand : il doit être plus haut avec un écart net (au moins une demi-tête)
        conforme = d.get("tete_la_plus_haute") == "B" and d.get("ecart") == "net"
        if not conforme and d.get("tete_la_plus_haute") != "non_applicable":
            ecarts.append(f"{fiches['personnages'][t['plus_petit']].get('nom', t['plus_petit'])} n'est pas "
                          f"nettement plus petit que {fiches['personnages'][t['plus_grand']].get('nom', t['plus_grand'])}"
                          f" : {d.get('explication', '')}")
            corrections.append((t.get("en") or "").strip())
    if not ecarts:
        return {"ok": True, "defauts": [], "ecarts": [], "correction_prompt": ""}
    return {"ok": False, "defauts": ["taille_relative_incorrecte"], "ecarts": ecarts,
            "correction_prompt": " ".join(corrections) + " Show a clear height difference between them."}


def _mains_en_pixels(image, journal, etiquette):
    """Rectangles des mains visibles (pixels), repérés par un modèle à vision."""
    from PIL import Image
    largeur, hauteur = Image.open(image).size
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_localisateur_mains.md"),
                     f"L'image fait {largeur} x {hauteur} pixels. Localise toutes les mains.",
                     cles=("mains",), images=[image], journal=journal, etiquette=f"{etiquette}_loc")
    boites = []
    for m in d["mains"] if isinstance(d["mains"], list) else []:
        try:
            x1, y1, x2, y2 = (float(m[k]) for k in ("x1", "y1", "x2", "y2"))
        except (KeyError, TypeError, ValueError):
            continue
        if max(x1, y1, x2, y2) <= 1.5:                      # fractions de l'image
            x1, x2, y1, y2 = x1 * largeur, x2 * largeur, y1 * hauteur, y2 * hauteur
        if x2 > x1 and y2 > y1:
            boites.append((max(int(x1), 0), max(int(y1), 0), min(int(x2), largeur), min(int(y2), hauteur)))
    return boites


def controle_mains(image, journal, etiquette, modele=None):
    """Chaque main entièrement visible a-t-elle bien cinq doigts ?

    Les vues d'ensemble ne se comptent pas : un modèle à vision compte « cinq » par habitude. On repère donc
    d'abord les mains, on recadre chacune en gros plan, puis un modèle énumère les doigts un par un ;
    c'est le code qui compte la liste énumérée et qui décide (défaut dès qu'une main entièrement visible
    n'a pas cinq doigts). Limite connue : le comptage reste imparfait, la validation humaine reste utile.
    """
    from pathlib import Path
    from PIL import Image
    mains = []
    for k, (x1, y1, x2, y2) in enumerate(_mains_en_pixels(image, journal, etiquette), 1):
        marge = int(0.25 * max(x2 - x1, y2 - y1))
        im = Image.open(image).convert("RGB")
        crop = im.crop((max(x1 - marge, 0), max(y1 - marge, 0), min(x2 + marge, im.width), min(y2 + marge, im.height)))
        cote = 1000.0 / max(crop.size)
        crop = crop.resize((int(crop.width * cote), int(crop.height * cote)), Image.LANCZOS)
        chemin = Path(journal) / f"{etiquette}_main{k}.png"
        Path(journal).mkdir(parents=True, exist_ok=True)
        crop.save(chemin)
        d = appeler_json(modele or CONFIG["roles"]["controleur_doigts"], lire("agents/prompt_controleur_mains.md"),
                         "Énumère les doigts de la main visible.", cles=("mains",), images=[chemin],
                         journal=journal, etiquette=f"{etiquette}_doigts{k}")
        for m in d["mains"] if isinstance(d["mains"], list) else []:
            if isinstance(m, dict) and isinstance(m.get("doigts_vus"), list):
                mains.append({"position": f"main {k} (x {x1}-{x2}, y {y1}-{y2})", "doigts": len(m["doigts_vus"]),
                              "main_entiere_visible": m.get("main_entiere_visible") is True})
    fautives = [m for m in mains if m["main_entiere_visible"] and m["doigts"] != 5]
    if not fautives:
        return {"ok": True, "defauts": [], "ecarts": [], "correction_prompt": "", "mains": mains}
    return {"ok": False, "defauts": ["mains_incorrectes"],
            "ecarts": [f"{m['position']} : {m['doigts']} doigts au lieu de 5" for m in fautives],
            "correction_prompt": "Draw each hand with exactly five fingers, one thumb and four fingers, natural hands.",
            "mains": mains}


def controle_coherence(references, image, contexte, journal, etiquette):
    """L'image est-elle cohérente (personnages, âge, décor, style) avec les images déjà validées ?"""
    contenu = (f"Les {len(references)} première(s) image(s) sont les références déjà validées. "
               f"La dernière image est la nouvelle image à contrôler.\n\n{contexte}")
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_coherence.md"), contenu,
                     cles=DEFAUTS_COHERENCE, images=[*references, image],
                     journal=journal, etiquette=etiquette)
    return _decider(d, DEFAUTS_COHERENCE)
