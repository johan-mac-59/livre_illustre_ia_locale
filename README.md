# Livres illustrés par IA locale

Générateur de livres illustrés pour enfants qui tourne **entièrement en local** sur une carte graphique grand public (12 Go de VRAM) : texte écrit ou adapté par des modèles de langage locaux (Ollama), images par ComfyUI, contrôles automatiques des dessins, mise en page d'un livre imprimable. Le projet part de souvenirs de famille réels : c'est la raison du « local », car ni les photos, ni les textes, ni les visages appris ne quittent la machine.

Ce dépôt est une **première publication partielle**. Il contient ce qui ne dépend d'aucune donnée personnelle :

| Dossier ou fichier | Contenu |
|---|---|
| [bilan_energie/](bilan_energie/) | Comparatif mesuré de l'énergie, du coût et du CO2 du travail fait en local contre le même travail dans le cloud (rapport PDF et Markdown, carrousel, données agrégées, méthode pour le refaire) |
| [agents/](agents/) | Les consignes données à chaque modèle (scénariste, correcteur, réécrivain, relecteur, contrôleurs d'images...), avec un fichier qui dit le rôle et l'état de chacune |
| [workflows/](workflows/) | Les workflows ComfyUI (format API) des dessinateurs utilisés |
| `llm.py`, `cadre.py`, `controles.py`, `generateur_image.py`, `lisibilite.py`, `montage.py` | Appels aux modèles locaux avec journal, cadre de contrôle des images auto-régulé (génération, contrôles, nouvelle graine), pilotage de ComfyUI, lisibilité du texte selon l'âge, montage PDF |

## Principes

- **Local d'abord** : aucune image ni aucun texte personnel ne passe par un service en ligne.
- **Tout dessin passe par un cadre de contrôle** : génération, contrôles automatiques (détails du personnage, mains, texte, taille relative), nouvelle graine si un contrôle échoue, rapport honnête des défauts persistants.
- **Robuste sans surveillance** : essais bornés, un contrôle interrompu est « non concluant », jamais « validé ».

## Ce qui n'est pas publié

Les photos, les textes des histoires, les planches de personnages, les LoRA de visages et les livres produits ; les modules qui contiennent encore des éléments propres aux personnages réels (entraînement de LoRA, planches, photos en dessins, mise en page). Ils seront généralisés puis ajoutés. Les fichiers de `agents/` peuvent faire référence à des modules absents de ce dépôt.

## Matériel et modèles

Testé sur une RTX 5070 (12 Go), un Core Ultra 7 265K, 64 Go de RAM. Les modèles ne sont pas fournis : leurs licences sont celles de leurs auteurs (certaines interdisent l'usage commercial).

## Licences

- Code : [MIT](LICENSE).
- Rapport et données du dossier `bilan_energie/` : [CC BY 4.0](bilan_energie/LICENSE.md).
- Consignes (`agents/`) et workflows : MIT, comme le code.
