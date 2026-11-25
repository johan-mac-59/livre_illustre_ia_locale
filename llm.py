"""Appels aux LLM locaux (Ollama) avec journal : un fichier JSON par appel."""
import base64
import itertools
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent
CONFIG = json.loads((RACINE / "config.json").read_text(encoding="utf-8"))
_compteur = itertools.count(1)


def lire(chemin):
    """Lit un fichier texte du projet (chemin relatif à la racine)."""
    return (RACINE / chemin).read_text(encoding="utf-8")


def _post(chemin, corps, timeout=3600):
    req = urllib.request.Request(
        CONFIG["ollama"] + chemin, data=json.dumps(corps).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def appeler(modele, systeme, contenu, *, json_mode=False, images=None,
            journal=None, etiquette="appel", temperature=0.3, max_tokens=None, reflexion=False):
    """Envoie un prompt à un modèle Ollama et retourne le texte de sa réponse.

    images : liste de chemins d'images (modèles à vision).
    journal : dossier où écrire le log de l'appel (prompt, réponse, durée).
    """
    user = {"role": "user", "content": contenu}
    if images:
        user["images"] = [base64.b64encode(Path(p).read_bytes()).decode() for p in images]
    corps = {
        "model": modele, "stream": False, "think": (reflexion if isinstance(reflexion, str) else bool(reflexion)), "keep_alive": "5m",       # reflexion : mode « réflexion » du modèle (coupé par défaut)
       
        "messages": [{"role": "system", "content": systeme}, user],
        "options": {"temperature": temperature, "num_ctx": 16384},
    }
    if max_tokens:
        corps["options"]["num_predict"] = max_tokens        # plafond de génération : coupe un modèle qui boucle
    if json_mode:
        corps["format"] = "json"
    debut = time.time()
    try:
        rep = _post("/api/chat", corps)
    except urllib.error.HTTPError:
        corps.pop("think")  # certains modèles refusent ce paramètre
        rep = _post("/api/chat", corps)
    texte = rep["message"]["content"]
    reflexion_txt = rep["message"].get("thinking") or ""
    if journal:
        dossier = Path(journal)
        dossier.mkdir(parents=True, exist_ok=True)
        nom = f"{next(_compteur):03d}_{etiquette}.json"
        (dossier / nom).write_text(json.dumps({
            "modele": modele, "etiquette": etiquette,
            "duree_s": round(time.time() - debut, 1),
            "images": [str(p) for p in (images or [])], "reflexion": reflexion if isinstance(reflexion, str) else bool(reflexion), "reflexion_caracteres": len(reflexion_txt),
            "systeme": systeme, "entree": contenu, "reponse": texte,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
    return texte


def appeler_json(modele, systeme, contenu, *, cles=(), essais=2, **kw):
    """Comme appeler(), mais retourne un dict JSON contenant les clés `cles`.

    Réessaie une fois si le JSON est invalide ou incomplet.
    """
    rappel = ""
    for essai in range(1, essais + 1):
        texte = appeler(modele, systeme, contenu + rappel, json_mode=True, **kw)
        try:
            d = json.loads(texte)
            if isinstance(d, dict) and all(c in d for c in cles):
                # certains modèles écrivent "true"/"false" entre guillemets : on les ramène à de vrais booléens
                return {k: (v.strip().lower() == "true" if isinstance(v, str) and v.strip().lower() in ("true", "false") else v)
                        for k, v in d.items()}
        except json.JSONDecodeError:
            pass
        rappel = f"\n\nRappel : réponds uniquement par un objet JSON avec les clés {list(cles)}."
    raise ValueError(f"JSON invalide ou incomplet après {essais} essais ({modele})")
