# Prompts des agents : rôle et état de chacun

Un fichier par rôle, nommé `prompt_<rôle>.md`. Ce tableau est tenu à jour à chaque ajout, renommage ou abandon d'un prompt.
**Statut déduit des références dans le code (qui charge quel prompt), pas d'une exécution.** Dernière mise à jour : 2026-11-19.

## Texte adapté : chaîne actuelle (`texte_auteur.py fidelite` puis `coherence`)

| Prompt | Rôle | Chargé par | État |
|---|---|---|---|
| `prompt_correcteur.md` | Correcteur : orthographe, grammaire, ponctuation, rien d'autre | étape 1, `corriger_fichier` | **actif** (gemma4:26b) |
| `prompt_reecrivain.md` | Réécrivain : adapte le texte pour un enfant de 6-7 ans, fidélité d'abord | étape 1, `adapter_fidele` ; banc `comparer_adaptation_brute.py` | **actif** (gemma4:31b) |
| `prompt_relecteur_ia.md` | Relecteur IA : compare l'adapté à l'original par paragraphe, vérifie le respect de la consigne, gravité majeur/mineur | étape 1, `verifier_fidelite` | **actif**, version V7 validée par l'auteur le 2026-11-20 (V4, conséquence écrite avant la gravité, plus : un détail de description retiré, remplacé ou rendu plus vague est majeur ; banc : `bench/variantes_relecteur/`, copie dans `v7_description_majeur.md`) ; modèle à choisir par l'auteur : gemma4:31b sans réflexion (10/18, 0 fausse alerte) ou qwen3.8 en réflexion low (18/18 vus, 2 fausses alertes sur 12) ; qwen3.6 et Mistral écartés |
| `prompt_coherence_texte.md` | Cohérence globale de l'histoire, texte adapté lu seul | étape 2 `coherence` ; aussi `coherence_livre` | **actif**, après validation humaine |

## Texte adapté : anciennes commandes, encore branchées mais remplacées dans la chaîne actuelle

| Prompt | Rôle | Chargé par | Remplacé par |
|---|---|---|---|
| `prompt_adaptateur.md` | Adaptation page par page avec seuils de lisibilité (chiffres imposés) | commandes `adapter` et `tout` | `prompt_reecrivain.md` |
| `prompt_extracteur_faits.md` | Liste les faits d'une page | `adapter`, `reprendre` | `prompt_relecteur_ia.md` (comparaison par paragraphe) |
| `prompt_controleur_faits.md` | Vérifie les faits manquants et les ajouts (beaucoup de faux positifs) | `adapter`, `reprendre` | `prompt_relecteur_ia.md` |
| `prompt_reprise.md` | Seconde passe sur la version retravaillée par l'auteur (boucle humaine, une version par tour) | commande `reprendre` | secondaire : la chaîne `fidelite` ne l'utilise pas |

## Livre illustré (`livre.py`)

| Prompt | Rôle | Chargé par | État |
|---|---|---|---|
| `prompt_scenariste_livre.md` | Écrit le texte de lecture et découpe en scènes à partir de l'histoire de l'auteur | `livre.py` | actif |
| `prompt_metteur_en_scene.md` | Description détaillée de chaque scénette (base du dessin) | `livre.py` | actif |
| `prompt_verificateur.md` | Vérifie le chapitre par rapport à la bible de l'auteur | `livre.py`, `orchestrateur.py`, banc | actif |

## Ancien pipeline (`orchestrateur.py`, noté « cassé : lit des fichiers de bible supprimés »)

| Prompt | Rôle | Chargé par | État |
|---|---|---|---|
| `prompt_scenariste.md` | Écrit un chapitre de 3 scènes à partir d'un souvenir brut | `orchestrateur.py`, `bench/bench.py` | **probablement obsolète** |
| `prompt_directeur_artistique.md` | Une illustration par scène (personnages, lieu, action) | `orchestrateur.py`, `bench/bench.py` | **probablement obsolète** (remplacé par `prompt_metteur_en_scene.md` dans `livre.py`) |
| `prompt_concepteur_visuel.md` | Fiches visuelles (catalogue de référence) | `fiches.py`, appelé par l'ancien orchestrateur | **probablement obsolète** : `fiches.py` reste importé pour d'autres fonctions |

## Contrôles d'images (`cadre.py`, `controles.py`, `traits.py`)

| Prompt | Rôle | Chargé par | État |
|---|---|---|---|
| `prompt_controleur_cadre.md` | Compte les personnes, repère le texte dans l'image | `cadre.py` | actif |
| `prompt_controleur_anatomie.md` | Défauts d'anatomie des personnages | `cadre.py` | actif |
| `prompt_controleur_traits.md` | Traits propres d'un personnage (questions fermées) | `traits.py` | actif |
| `prompt_controleur_scene.md` | Scène conforme à la description et aux fiches | `controles.py` | actif |
| `prompt_controleur_coherence.md` | Cohérence graphique avec des images de référence validées | `controles.py` | actif |
| `prompt_controleur_taille.md` | Taille relative de deux personnages | `controles.py` | actif |
| `prompt_controleur_mains.md` | Nombre de doigts d'une main recadrée | `controles.py` | actif |
| `prompt_localisateur_mains.md` | Repère les mains dans l'image (rectangles) | `controles.py` | actif |
| `prompt_controleur_style.md` | Style (gouache et lavis) respecté | `cadre.py`, banc LoRA | actif |
| `prompt_controleur_vetements.md` | Compare les vêtements à des images de référence | banc `rejouer_vetements.py` seulement | **expérimental, non branché au cadre** |

## Photos et LoRA

| Prompt | Rôle | Chargé par | État |
|---|---|---|---|
| `prompt_descripteur_photo.md` | Décrit une photo réelle pour vérifier la fidélité du dessin | `photos.py` | actif |
| `prompt_controleur_photo.md` | Dessin fidèle à la photo d'origine (fidélité, style) | `cadre.py` | actif |
| `prompt_controleur_coherence_photo.md` | Cohérence d'un personnage d'une image de l'histoire à l'autre (dessins tirés de photos) | `cadre.py` | actif |
| `prompt_legendeur_lora.md` | Légende des images d'entraînement d'un LoRA | `lora.py` | actif |

## À décider par l'auteur
- Les trois prompts de l'ancien orchestrateur (`scenariste`, `directeur_artistique`, `concepteur_visuel`) et le script `orchestrateur.py` lui-même : à supprimer ou à garder comme archive.
- Les quatre prompts des anciennes commandes du texte (`adaptateur`, `extracteur_faits`, `controleur_faits`, `reprise`) : à supprimer si les commandes `adapter`, `tout` et `reprendre` sont abandonnées au profit de `fidelite` et `coherence`.
- `prompt_controleur_vetements.md` : à brancher au cadre ou à retirer.
