# Livre illustré IA locale

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13">
  <img src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" alt="Ollama">
  <img src="https://img.shields.io/badge/ComfyUI-1F2937?style=for-the-badge" alt="ComfyUI">
  <img src="https://img.shields.io/badge/ReportLab-PDF-E34F26?style=for-the-badge" alt="ReportLab">
  <img src="https://img.shields.io/badge/Pillow-3776AB?style=for-the-badge" alt="Pillow">
  <img src="https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=uv&logoColor=white" alt="uv">
</p>

**Générateur de livres illustrés pour enfants, tournant entièrement en local sur une carte graphique grand public (12 Go de VRAM).** Texte écrit ou adapté par des modèles de langage locaux, dessins par des modèles d'image locaux, contrôles automatiques de chaque image, mise en page d'un livre imprimable. Le projet part de souvenirs de famille réels : c'est la raison du « local », car ni les photos, ni les textes, ni les visages appris ne quittent la machine.

**Première publication partielle** · 📊 **[Bilan énergie : local contre cloud](bilan_energie/)**

---

## 📌 Présentation

### 🎯 Le défi
Faire un livre pour chaque enfant d'une famille, avec leurs vraies histoires et leurs vrais visages dessinés, sans envoyer une seule photo à un service en ligne, et sans surveiller chaque étape.

### 🛠️ La solution
Une chaîne de modèles locaux où chaque rôle a sa consigne (scénariste, correcteur, réécrivain, relecteur, concepteur visuel, contrôleurs d'images). Chaque dessin passe par un **cadre de contrôle auto-régulé** : génération, contrôles automatiques (détails du personnage, mains, texte, taille relative), nouvelle graine si un contrôle échoue, rapport honnête des défauts persistants. Le but est un livre complet de bout en bout, que l'humain valide à la fin plutôt qu'étape par étape.

### 💡 Ce qui la distingue
- **Local d'abord** : aucun texte ni aucune image personnelle ne passe par le cloud.
- **Robuste sans surveillance** : essais bornés, un contrôle interrompu est « non concluant », jamais « validé ».
- **Mesuré** : l'énergie, le coût et le CO2 du travail sont comparés au même travail dans le cloud.

---

## 🚀 Contenu du dépôt

| Dossier ou fichier | Contenu |
|---|---|
| **[bilan_energie/](bilan_energie/)** | Comparatif mesuré de l'énergie, du coût et du CO2 du travail local contre le cloud : rapport (PDF et Markdown), carrousel, données agrégées, méthode pour le refaire |
| **[agents/](agents/)** | Les consignes de chaque modèle, avec un fichier qui dit le rôle et l'état de chacune |
| **[workflows/](workflows/)** | Les workflows ComfyUI (format API) des dessinateurs utilisés |
| `llm.py` | Appels aux modèles de texte et de vision locaux (Ollama), avec journal d'appels |
| `cadre.py`, `controles.py` | Cadre de contrôle des images auto-régulé et contrôles |
| `generateur_image.py` | Pilotage de ComfyUI par son API |
| `lisibilite.py` | Lisibilité d'un texte selon l'âge de l'enfant |
| `montage.py` | Montage d'un PDF de livre illustré |

---

## 📊 Résultat du bilan énergie

Le même travail (4 modèles de visages entraînés, plus de 1 300 images, plus de 5 000 appels de texte, deux livres de trois histoires) fait en local puis chiffré dans le cloud :

| | Local | Cloud |
|---|---|---|
| Coût TTC | **35 €** (11 € d'amortissement avec des durées de vie ambitieuses) | **81 €** en API, **53 à 97 €** en GPU loué |
| Énergie | 20,2 kWh | 9,7 à 18,8 kWh |
| CO2 | 1,05 kg (réseau français) | 3,7 à 7,2 kg (réseau américain supposé) |

Ces chiffres reposent sur des hypothèses explicites, détaillées avec leurs sources et leurs limites dans [le rapport](bilan_energie/).

---

## 🔒 Ce qui n'est pas publié

Les photos, les textes des histoires, les planches de personnages, les visages appris (LoRA) et les livres produits restent privés. Les modules qui contiennent encore des éléments propres aux personnages réels (entraînement de LoRA, planches, photos en dessins, mise en page) seront généralisés puis ajoutés. Les consignes de `agents/` peuvent donc citer des modules absents de ce dépôt.

---

## 🖥️ Matériel et modèles

Testé sur une RTX 5070 (12 Go de VRAM), un Core Ultra 7 265K et 64 Go de RAM. Les modèles ne sont pas fournis : leurs licences sont celles de leurs auteurs, et certaines interdisent l'usage commercial.

**Prérequis** : Python 3.13, [Ollama](https://ollama.com), [ComfyUI](https://github.com/comfyanonymous/ComfyUI), `pip install -r requirements.txt`.

---

## 📄 Licences

- Code, consignes (`agents/`) et workflows : [MIT](LICENSE).
- Rapport et données de `bilan_energie/` : [CC BY 4.0](bilan_energie/LICENSE.md).
