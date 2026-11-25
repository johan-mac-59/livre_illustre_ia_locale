"""Dessinateur : génère une image via l'API locale de ComfyUI.

Le workflow (API format) est un fichier de workflows/. Le code remplace le
prompt, la graine et la taille, envoie le tout à ComfyUI, attend, récupère
l'image et la range dans sorties/images/. La VRAM est libérée avant (Ollama)
et après (ComfyUI), car LLM et diffusion ne tiennent pas ensemble en 12 Go.

Usage :
    python generateur_image.py --workflow klein4b_txt2img --prompt "..." --seed 1
"""
import argparse
import copy
import hashlib
import json
import re
import time
import uuid
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent
COMFY = "http://127.0.0.1:8188"
OLLAMA = "http://localhost:11434"


def _requete(url, corps=None, timeout=60):
    data = json.dumps(corps).encode() if corps is not None else None
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def decharger_ollama():
    """Décharge tous les modèles Ollama chargés (keep_alive 0)."""
    actifs = json.loads(_requete(OLLAMA + "/api/ps")).get("models", [])
    for m in actifs:
        _requete(OLLAMA + "/api/generate", {"model": m["name"], "keep_alive": 0})
    return [m["name"] for m in actifs]


def decharger_comfy():
    """Demande à ComfyUI de libérer modèles et VRAM."""
    _requete(COMFY + "/free", {"unload_models": True, "free_memory": True})


def televerser(chemin):
    """Envoie une image à ComfyUI (dossier input) et retourne le nom sous lequel il la connaît."""
    chemin = Path(chemin)
    donnees = chemin.read_bytes()
    nom = f"atelier_{hashlib.sha1(donnees).hexdigest()[:12]}{chemin.suffix}"
    limite = uuid.uuid4().hex
    corps = (f'--{limite}\r\nContent-Disposition: form-data; name="image"; filename="{nom}"\r\n'
             f"Content-Type: image/png\r\n\r\n").encode() + donnees + (
             f'\r\n--{limite}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue'
             f"\r\n--{limite}--\r\n").encode()
    req = urllib.request.Request(COMFY + "/upload/image", data=corps,
                                 headers={"Content-Type": f"multipart/form-data; boundary={limite}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["name"]


def preparer(workflow, prompt, seed, largeur, hauteur, prefixe, negatif="", images=(), encodeur=None, lora=None,
             modele=None, resolution=None):
    """Remplit un workflow API : prompt, graine, taille, préfixe de fichier, images de référence.

    images : noms d'images déjà téléversées. Les nœuds IMAGEk / ECHELLEk au-delà du nombre
    d'images fournies sont retirés, ainsi que les entrées qui y étaient reliées.
    encodeur : nom du fichier d'encodeur de texte à utiliser à la place de celui du workflow (comparaisons).
    lora : (fichier dans models/loras, force) pour le nœud LoraLoaderModelOnly du workflow ; force 0 = sans LoRA.
    modele : fichier de models/diffusion_models à la place de celui du workflow (ex. LoRA déjà fusionné en fp8,
    lu avec weight_dtype « default »).
    """
    w = copy.deepcopy(workflow)
    for cle, noeud in list(w.items()):
        m = re.fullmatch(r"(?:IMAGE|ECHELLE)(\d)", noeud.get("_meta", {}).get("title", ""))
        if m and int(m.group(1)) > len(images):
            del w[cle]
    for noeud in w.values():
        for k, v in list(noeud["inputs"].items()):
            if isinstance(v, list) and v and v[0] not in w:
                del noeud["inputs"][k]
    for noeud in w.values():
        c, i = noeud["class_type"], noeud["inputs"]
        titre = noeud.get("_meta", {}).get("title", "")
        m = re.fullmatch(r"IMAGE(\d)", titre)
        if c == "LoadImage" and m:
            i["image"] = images[int(m.group(1)) - 1]
        elif c == "TextEncodeQwenImage21":
            i["prompt"], i["negative_prompt"] = prompt, negatif
            if resolution:                           # côté d'un carré de même surface : la taille de sortie suit (résolution² pixels)
                i["resolution"] = resolution
        elif c == "CLIPTextEncode" and titre == "NEGATIF":
            i["text"] = negatif
        elif c == "CLIPTextEncode":
            i["text"] = prompt
        elif c == "TextEncodeQwenImageEditPlus" and titre == "PROMPT":
            i["prompt"] = prompt
        elif c == "TextEncodeQwenImageEditPlus" and titre == "NEGATIF":
            i["prompt"] = negatif
        elif c == "RandomNoise":
            i["noise_seed"] = seed
        elif c == "KSampler":
            i["seed"] = seed
        elif c in ("EmptyFlux2LatentImage", "Flux2Scheduler", "EmptySD3LatentImage", "EmptyLatentImage"):
            i["width"], i["height"] = largeur, hauteur
        elif c == "SaveImage":
            i["filename_prefix"] = prefixe
        elif c == "CLIPLoader" and encodeur:
            i["clip_name"] = encodeur
        elif c == "LoraLoaderModelOnly" and lora:
            i["lora_name"], i["strength_model"] = nom_comfy("LoraLoaderModelOnly", "lora_name", lora[0]), lora[1]
        elif c == "UNETLoader" and modele:
            i["unet_name"], i["weight_dtype"] = nom_comfy("UNETLoader", "unet_name", modele), "default"
    return w


def nom_comfy(noeud, entree, nom):
    """Nom de fichier tel que ComfyUI le liste (sous Windows, sous-dossier séparé par « \\ » et non « / »)."""
    try:
        info = json.loads(_requete(f"{COMFY}/object_info/{noeud}"))
        noms = info[noeud]["input"]["required"][entree][0]
    except Exception:
        return nom
    cle = nom.replace("\\", "/")
    return next((n for n in noms if n.replace("\\", "/") == cle), nom)


def generer(nom_workflow, prompt, seed=0, largeur=1024, hauteur=1024,
            sortie=None, timeout=3600, negatif="", images=(), garder_modele=False, encodeur=None, lora=None,
            modele=None, resolution=None):
    """Génère une image et retourne le chemin du PNG sauvegardé.

    garder_modele=True : ne décharge pas ComfyUI après l'image, pour enchaîner une série avec le
    même modèle sans le recharger (appeler decharger_comfy() à la fin de la série).
    """
    workflow = json.loads((RACINE / "workflows" / f"{nom_workflow}.json").read_text(encoding="utf-8"))
    prefixe = f"atelier_bd/{nom_workflow}"
    noms = [televerser(p) for p in images]
    w = preparer(workflow, prompt, seed, largeur, hauteur, prefixe, negatif, noms, encodeur, lora, modele, resolution)

    decharger_ollama()
    retour = json.loads(_requete(COMFY + "/prompt", {"prompt": w}))
    id_prompt = retour["prompt_id"]

    debut = time.time()
    while True:
        histoire = json.loads(_requete(f"{COMFY}/history/{id_prompt}"))
        if id_prompt in histoire:
            break
        if time.time() - debut > timeout:
            raise TimeoutError(f"ComfyUI n'a pas fini en {timeout}s")
        time.sleep(1)

    resultat = histoire[id_prompt]
    if resultat["status"]["status_str"] != "success":
        raise RuntimeError(json.dumps(resultat["status"], ensure_ascii=False)[:1000])
    image = next(img for sortie_n in resultat["outputs"].values() for img in sortie_n.get("images", []))
    params = urllib.parse.urlencode({k: image[k] for k in ("filename", "subfolder", "type")})
    png = _requete(f"{COMFY}/view?{params}")

    dossier = RACINE / "sorties" / "images"
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = Path(sortie) if sortie else dossier / f"{nom_workflow}_seed{seed}.png"
    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_bytes(png)
    chemin.with_suffix(".json").write_text(json.dumps({
        "workflow": nom_workflow, "encodeur": encodeur, "prompt": prompt, "seed": seed,
        "largeur": largeur, "hauteur": hauteur,
        "duree_s": round(time.time() - debut, 1),
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    if not garder_modele:
        decharger_comfy()
    return chemin


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--largeur", type=int, default=1024)
    p.add_argument("--hauteur", type=int, default=1024)
    a = p.parse_args()
    t = time.time()
    print(generer(a.workflow, a.prompt, a.seed, a.largeur, a.hauteur), f"({time.time() - t:.0f}s)")
