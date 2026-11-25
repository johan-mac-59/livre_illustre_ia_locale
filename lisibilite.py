"""Lisibilité d'un texte pour un enfant lecteur débutant : mesures par le code (pas de modèle).

Phrases courtes, mots courts. Les limites dépendent de l'âge ; elles servent de contrôle du texte de lecture
(niveau scène) et sont reportées dans le rapport de génération.
"""
import re

# âge -> (moyenne de mots par phrase max, phrase la plus longue max, % de mots longs max)
LIMITES = {6: (8.0, 14, 8.0), 7: (9.0, 16, 9.0), 8: (11.0, 18, 10.0)}
LIMITES_DEFAUT = (13.0, 22, 12.0)
MOT_LONG = 9      # lettres


def analyser(texte, exclus=()):
    """Mesures : mots, phrases, mots par phrase (moyenne et max), part de mots longs.

    exclus : mots qui ne comptent pas comme mots longs (noms propres de l'histoire : un prénom long reste lisible)."""
    phrases = [p for p in re.split(r"(?<=[.!?…])\s+|\n+", texte.replace("»", "» ")) if re.search(r"\w", p)]
    mots = re.findall(r"[\wÀ-ÿ]+(?:['’-][\wÀ-ÿ]+)*", texte)
    par_phrase = [len(re.findall(r"[\wÀ-ÿ]+", p)) for p in phrases] or [0]
    exclus = {e.lower() for e in exclus}
    longs = [m for m in mots if len(re.sub(r"[^\wÀ-ÿ]", "", m)) >= MOT_LONG and m.lower() not in exclus]
    return {"mots": len(mots), "phrases": len(phrases), "mots_par_phrase": round(sum(par_phrase) / len(par_phrase), 1),
            "phrase_max": max(par_phrase), "mots_longs_pct": round(100 * len(longs) / max(len(mots), 1), 1),
            "mots_longs": longs}


def problemes(texte, age, mots_min, mots_max, exclus=()):
    """Liste de problèmes (vide si le texte convient à l'âge), formulés pour être renvoyés au rédacteur."""
    moy_max, phrase_max, longs_max = LIMITES.get(age, LIMITES_DEFAUT)
    m = analyser(texte, exclus)
    res = []
    if not mots_min <= m["mots"] <= mots_max:
        res.append(f"{m['mots']} mots au lieu de {mots_min} à {mots_max}")
    if m["mots_par_phrase"] > moy_max:
        res.append(f"phrases trop longues en moyenne ({m['mots_par_phrase']} mots, maximum {moy_max}) : fais des phrases plus courtes")
    if m["phrase_max"] > phrase_max:
        res.append(f"une phrase de {m['phrase_max']} mots (maximum {phrase_max}) : coupe-la")
    if m["mots_longs_pct"] > longs_max:
        res.append(f"trop de mots longs ({m['mots_longs_pct']} %, maximum {longs_max} %) : {', '.join(m['mots_longs'][:5])} : choisis des mots plus simples")
    return res
