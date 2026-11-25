"""Cadre de contrôle auto-régulé : tout dessin passe par produire().

L'orchestrateur change de niveau selon ce qu'on crée (personnage, scénette, livre) et les contrôles
se CUMULENT : un niveau applique ses propres contrôles et ceux des niveaux inférieurs.

    personnage : détails propres au personnage (controles.json), mains à 5 doigts, nombre de personnes, pas de texte
    scenette   : + scène conforme aux fiches, taille relative ; dessin tiré d'une photo : fidélité à la photo, style
    livre      : + cohérence avec les images déjà validées du livre ; dessins tirés de photos : chaque personne reste
                 reconnaissable (visage, cheveux, proportions, âge), les vêtements peuvent changer

Boucle : génération -> contrôles -> si KO, nouveau dessin (autre graine, corrections réinjectées) -> limite d'essais
-> on garde la tentative qui a le moins de défauts et on le dit (rapport honnête, jamais de défaut caché).
Chaque contrôle reçoit un contexte (dict) et retourne {ok, defauts, ecarts, correction_prompt}, ou None si non applicable.
Ajouter un contrôle = écrire une fonction décorée par @controle(niveau, nom).
"""
import json
import time
from pathlib import Path

NIVEAUX = ("personnage", "scenette", "livre")
CONTROLES = []          # (niveau, nom, fonction)


def controle(niveau, nom):
    def enregistrer(f):
        CONTROLES.append((niveau, nom, f))
        return f
    return enregistrer


def actifs(niveau):
    """Contrôles du niveau demandé et de tous les niveaux inférieurs (cumul)."""
    n = NIVEAUX.index(niveau)
    return [(nom, f) for niv, nom, f in CONTROLES if NIVEAUX.index(niv) <= n]


def _res(defauts, ecarts=None, correction=""):
    return {"ok": not defauts, "defauts": list(defauts), "ecarts": list(ecarts or defauts),
            "correction_prompt": correction if defauts else ""}


# --- Niveau personnage -------------------------------------------------------

@controle("personnage", "details_personnage")
def _details(ctx):
    if not all(k in ctx for k in ("perso", "serie", "cle")):
        return None
    import planches
    return _res(planches.controle_vue(ctx["perso"], ctx["serie"], ctx["cle"], ctx["image"], ctx["journal"]))


@controle("personnage", "mains")
def _mains(ctx):
    import controles
    return controles.controle_mains(ctx["image"], ctx["journal"], f"{ctx['etiquette']}_mains")


DEFAUTS_ANATOMIE = ("visage_ou_tete_double", "yeux_ou_oreilles_en_trop_ou_deformes", "bras_en_trop_ou_manquant",
                    "jambes_en_trop_ou_manquantes", "membres_fusionnes_ou_deformes", "proportions_aberrantes")


@controle("personnage", "anatomie")
def _anatomie(ctx):
    """Anatomie humaine de base, valable pour tout personnage (les mains ont leur contrôle dédié)."""
    import controles
    from llm import CONFIG, appeler_json, lire
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_anatomie.md"), "Contrôle l'anatomie des personnages.",
                     cles=DEFAUTS_ANATOMIE, images=[ctx["image"]], journal=ctx["journal"], etiquette=f"{ctx['etiquette']}_anatomie")
    return controles._decider(d, DEFAUTS_ANATOMIE)


@controle("personnage", "personnes_et_texte")
def _personnes_texte(ctx):
    from llm import CONFIG, appeler_json, lire
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_cadre.md"), "Compte les personnes et cherche du texte.",
                     cles=("nombre_personnes", "texte_visible"), images=[ctx["image"]], journal=ctx["journal"],
                     etiquette=f"{ctx['etiquette']}_cadre")
    defauts, ecarts = [], []
    attendu = ctx.get("nb_personnes")
    if attendu is not None and d["nombre_personnes"] != attendu:
        defauts.append("nombre_de_personnes")
        ecarts.append(f"{d['nombre_personnes']} personne(s) au lieu de {attendu}")
    if d["texte_visible"] is True:
        defauts.append("texte_visible")
        ecarts.append("du texte est visible dans l'image")
    return _res(defauts, ecarts, f"Exactly {attendu} person(s) in the image, no written text anywhere." if attendu else
                "No written text anywhere in the image.")


# --- Niveau scénette ---------------------------------------------------------

@controle("scenette", "scene")
def _scene(ctx):
    if "illustration" not in ctx:
        return None
    import controles
    return controles.controle_scene(ctx["image"], ctx["illustration"], ctx["fiches"], ctx["journal"], f"{ctx['etiquette']}_scene")


@controle("scenette", "taille_relative")
def _taille(ctx):
    if "illustration" not in ctx:
        return None
    import controles
    return controles.controle_taille(ctx["image"], ctx["illustration"], ctx["fiches"], ctx["journal"], f"{ctx['etiquette']}_taille")


DEFAUTS_PHOTO = ("personne_manquante", "personne_en_trop", "age_different", "pose_ou_action_differente",
                 "vetements_ou_cheveux_differents", "decor_different", "objet_important_manquant", "cadrage_different")
DEFAUTS_STYLE = ("rendu_photographique", "style_non_conforme", "visage_deforme", "inquietant")


@controle("scenette", "fidelite_photo")
def _fidelite_photo(ctx):
    """Dessin tiré d'une photo : mêmes personnes, poses, vêtements, décor et cadrage que la photo (deux images)."""
    if "photo" not in ctx:
        return None
    import controles
    from llm import CONFIG, appeler_json, lire
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_photo.md"),
                     f"## Description de la photo\n{ctx.get('description_photo', '')}",
                     cles=DEFAUTS_PHOTO, images=[ctx["photo"], ctx["image"]], journal=ctx["journal"],
                     etiquette=f"{ctx['etiquette']}_fidelite")
    return controles._decider(d, DEFAUTS_PHOTO)


@controle("scenette", "style_photo")
def _style_photo(ctx):
    """Dessin tiré d'une photo : c'est bien un dessin, dans le style demandé (le dessin seul)."""
    if "photo" not in ctx or "style" not in ctx:
        return None
    import controles
    import photos
    from llm import CONFIG, appeler_json, lire
    d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_style.md"),
                     f"Style demandé : {photos.STYLES[ctx['style']]['fr']}", cles=DEFAUTS_STYLE, images=[ctx["image"]],
                     journal=ctx["journal"], etiquette=f"{ctx['etiquette']}_style")
    return controles._decider(d, DEFAUTS_STYLE)


# --- Niveau livre ------------------------------------------------------------

@controle("livre", "coherence")
def _coherence(ctx):
    if not ctx.get("references"):
        return None
    import controles
    return controles.controle_coherence(ctx["references"], ctx["image"], ctx.get("contexte_coherence", ""),
                                        ctx["journal"], f"{ctx['etiquette']}_coh")


DEFAUTS_COHERENCE_PHOTO = ("visage_different", "cheveux_differents", "proportions_differentes", "age_different",
                           "style_different")


@controle("livre", "coherence_personnages")
def _coherence_personnages(ctx):
    """Dessins tirés de photos d'une même histoire : chaque personne reste reconnaissable (visage, cheveux, proportions,
    âge, style) d'un dessin validé à l'autre ; les vêtements peuvent changer. Une comparaison par dessin de référence.

    ctx["references_personnages"] : [(dessin validé, texte « qui est où » dans les deux dessins)].
    """
    refs = ctx.get("references_personnages")
    if not refs:
        return None
    import controles
    from llm import CONFIG, appeler_json, lire
    defauts, ecarts, corrections = [], [], []
    for k, (ref, qui) in enumerate(refs, 1):
        d = appeler_json(CONFIG["roles"]["controleur"], lire("agents/prompt_controleur_coherence_photo.md"),
                         f"## Personnes communes aux deux dessins\n{qui}", cles=DEFAUTS_COHERENCE_PHOTO,
                         images=[ref, ctx["image"]], journal=ctx["journal"], etiquette=f"{ctx['etiquette']}_cohp{k}")
        r = controles._decider(d, DEFAUTS_COHERENCE_PHOTO)
        defauts += [x for x in r["defauts"] if x not in defauts]
        ecarts += [f"face à {Path(ref).name} : {e}" for e in (r["ecarts"] or r["defauts"])] if not r["ok"] else []
        corrections += [r["correction_prompt"]] if r["correction_prompt"] else []
    return _res(defauts, ecarts, " ".join(corrections))


# --- Boucle ------------------------------------------------------------------

def verifier(niveau, ctx, arret=False):
    """Passe tous les contrôles actifs sur ctx['image'] ; retourne {nom: résultat} (non applicables omis)."""
    sortie = {}
    for nom, f in actifs(niveau):
        try:
            r = f(ctx)
        except Exception as e:      # délai, JSON invalide, modèle indisponible : jamais validé ni planté
            r = {"ok": False, "defauts": ["controle_non_concluant"], "ecarts": [f"contrôle « {nom} » non concluant : {e}"],
                 "correction_prompt": ""}
        if r is not None:
            sortie[nom] = r
            if arret and not r["ok"]:      # mode rapide : on s'arrête au premier défaut (les contrôles restent cumulés)
                break
    return sortie


def produire(niveau, generer, ctx, essais=5, graine=21, pas=10, lot=1, rapide=False):
    """Génère jusqu'à validation. `generer(graine, corrections) -> chemin` dessine UNE image neuve.

    ctx : journal, etiquette, + ce que les contrôles du niveau utilisent (perso/serie/cle, nb_personnes,
    illustration/fiches, references...). Retourne {image, ok, defauts, tentatives} ; défauts = ceux de la
    tentative gardée (la moins défectueuse, la plus récente à égalité), vide si validée.

    lot > 1 : on dessine `lot` images d'affilée (le dessinateur reste chargé), on le décharge UNE fois, puis le contrôleur
    examine les images dans l'ordre et on s'arrête à la première validée ; `essais` compte les images.
    rapide : un contrôle ne passe plus les suivants dès qu'un défaut est trouvé (gain de temps, moins de corrections remontées).
    """
    tentatives, corrections, t = [], [], 0
    while t < essais and not (tentatives and not tentatives[-1]["defauts"]):
        n = min(lot, essais - t)
        images = []
        for _ in range(n):
            t += 1
            s = graine + pas * (t - 1)
            t0 = time.time()
            images.append((t, s, Path(generer(s, list(corrections))), round(time.time() - t0)))
        if lot > 1:
            import generateur_image
            generateur_image.decharger_comfy()
        for num, s, image, duree_gen in images:
            t1 = time.time()
            resultats = verifier(niveau, {**ctx, "image": image, "etiquette": f"{ctx['etiquette']}_t{num}"}, arret=rapide)
            defauts = [f"{nom} : {e}" for nom, r in resultats.items() if not r["ok"] for e in r["ecarts"]]
            tentatives.append({"tentative": num, "graine": s, "image": str(image), "defauts": defauts,
                               "duree_generation_s": duree_gen, "duree_controles_s": round(time.time() - t1)})
            if not defauts:
                break
            print(f"  contrôle KO, essai {num}/{essais} ({'; '.join(defauts)})")
            corrections += [r["correction_prompt"] for r in resultats.values() if not r["ok"] and r["correction_prompt"]]
    meilleure = min(reversed(tentatives), key=lambda x: len(x["defauts"]))
    ok = not meilleure["defauts"]
    if not ok:
        print(f"  {ctx['etiquette']} : {len(tentatives)} essais, défaut(s) persistant(s) : {'; '.join(meilleure['defauts'])}")
    rapport = {"niveau": niveau, "controles": [n for n, _ in actifs(niveau)], "ok": ok, "tentatives": tentatives}
    Path(ctx["journal"]).mkdir(parents=True, exist_ok=True)
    (Path(ctx["journal"]) / f"rapport_{ctx['etiquette']}.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"image": meilleure["image"], "ok": ok, "defauts": meilleure["defauts"], "tentatives": tentatives}
