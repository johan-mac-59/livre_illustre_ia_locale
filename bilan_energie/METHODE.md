# Méthode du bilan énergie, coût et CO2 : refaire et poursuivre le calcul

Ce document permet de **dupliquer** le bilan (autre machine, autre projet) et de le **poursuivre** (nouvelles histoires, nouveaux entraînements, point énergétique final). Il ne contient aucune donnée personnelle ; il est publiable tel quel.

## 1. Ce que le bilan calcule

Pour tout le travail du projet (entraînements de LoRA, images, texte), en local et dans un scénario cloud équivalent : énergie (Wh), coût (€ TTC), CO2 (kg), amortissement de la machine, transferts de données, coût de la mission de calcul elle-même. Rapport : `bilan_energie.md` (privé, versionné) et `sorties/rapport/bilan_energie_public.md` (édition publique anonymisée).

## 2. Chaîne de production du rapport

| Étape | Commande | Produit |
|---|---|---|
| Calcul et rapport | `python bilan_energie.py` | `bilan_energie.md`, édition publique, `chiffres_cles.json`, archive des données |
| PDF du rapport | `python bilan_pdf.py sorties/rapport/bilan_energie_public.md sorties/rapport/bilan_energie_public.pdf` | PDF (Chrome sans fenêtre, sans dépendance) |
| Carrousel LinkedIn | `python carrousel.py --lien <URL>` | `sorties/rapport/carrousel_energie.pdf` (7 pages 1080 x 1350) |
| Mesure de puissance | `python mesure_energie.py echantillonner sorties/energie/<nom>.csv` puis `bilan` | Wh GPU mesurés, Wh CPU estimés |

Le rapport, le PDF public, le carrousel et le post se régénèrent depuis les mêmes chiffres : ne jamais retaper un chiffre à la main.

## 3. Données d'entrée et où elles vivent

Tout ce qui sert au calcul est relu à chaque exécution ; une **copie datée** est écrite dans `sorties/energie/archives/<date>/` (voir §5).

| Donnée | Source dans le projet | Contenu utilisé |
|---|---|---|
| Puissance du GPU et du CPU | `sorties/energie/*.csv` (échantillonneur `mesure_energie.py`, une ligne par seconde ou deux : heure, W du GPU, % GPU, % CPU) | GPU en images (201 W à plus de 90 % d'utilisation), en entraînement (208 W), texte (65 W de moyenne) |
| Durées d'entraînement des LoRA | `dossier privé/lora/<lora>/qwen2512/bilan.json` (`etapes.entrainement.duree_s`) ; sinon pas x secondes par pas du journal | Secondes par entraînement |
| Dessins générés pour les jeux d'entraînement | `sorties/photos_essai/<jeu>/resultats.json` (une entrée par dessin, `duree_s`) | Nombre et durée |
| Tests des LoRA | `sorties/lora_test/<test>/resultats.json` | Nombre et durée des images de test |
| Images des livres | `sorties/scenes_<histoire>/**/*.json` (`duree_s`) ; les images présentes sans durée sont comptées à la durée moyenne | Nombre et durée |
| Images écrasées par une relance de même nom | `sorties/*.log` (journaux de relance, 3 graines par relance) | Comptées en plus (voir `ECRASEES` dans `bilan_energie.py`) |
| Texte (modèles locaux) | journaux d'appels `**/appel*|journal*|logs/**/*.json` (`modele`, `duree_s`, `systeme`, `contenu`, `reponse`) | Appels, durée, tokens estimés (3,5 caractères par token) |
| Images utilisées dans les livres | `dossier privé/histoires/<n>/images/*_provenance.json` (hors éléments de composition) | Nombre d'images retenues |
| Appels à Claude Code (mission) | les journaux de session de l'outil et `subagents/` | Appels et tokens exacts |

Paramètres (tarifs, facteurs d'émission, puissances, accélération du GPU de datacenter, TVA, change) : constantes en tête de `bilan_energie.py`, chacune avec sa source dans la section Sources du rapport.

## 4. Principes de calcul

- **Énergie locale** = durée enregistrée x puissance (GPU mesuré + CPU estimé par l'utilisation : 15 W au repos, 125 W à pleine charge). Reste du PC ignoré (choix assumé, signalé dans les limites).
- **Cloud équivalent** : mêmes images, mêmes pas, mêmes appels. Deux scénarios : API payante (prix par pas et par mégapixel) et location d'un GPU (prix horaire / accélération 4 à 8 fois). Énergie : durée / accélération x puissance x PUE. Texte : 0,24 à 0,34 Wh par requête.
- **CO2** : kWh x facteur du réseau (France 52 g/kWh ; États-Unis 384 g/kWh pour le cloud, lieu supposé).
- **Amortissement** : pour chaque composant, prix / (durée de vie propre x heures de calcul par jour), additionné puis imputé aux heures du projet ; durées = garantie constructeur publiée (référence), comparée à 3 ans comptables et aux guides ; référence 4 h par jour (composants et durées : `COMPOSANTS` en tête de `bilan_energie.py`).
- **Transferts** : Go x kWh/Go (valeur de l'Arcep pour le réseau fixe français, 0,02), même facteur pour les deux côtés.
- **Mise au point (coût fixe) séparée de l'usage (production)** : entraînements, essais, bancs de texte d'un côté ; images et texte livrés de l'autre.
- **Exclus et cités** : entraînement des modèles eux-mêmes, fabrication du matériel (non calculables). **Annexe** : coût de la mission de calcul (hors projet).

## 5. Garder les traces

À chaque exécution, `bilan_energie.py` écrit dans `sorties/energie/archives/<date>/` :

- `donnees_calcul.json` : paramètres et toutes les valeurs d'entrée agrégées (durées, nombres d'images, tokens, appels) ;
- `donnees_calcul_anonymisees.json` : même contenu, sans donnée personnelle (publiable) ;
- `mesures/` : copie des fichiers de puissance ;
- `chiffres_cles.json` et une copie de `bilan_energie.py` (le calcul exact de la date).

Ces archives sont **hors git** (le dossier `sorties/` n'est pas versionné) : les sauvegarder avec le reste des données du projet. Elles permettent de refaire le rapport même si des dossiers d'origine sont supprimés ou vidés ; avant tout nettoyage de dossier de résultats, **relancer le bilan** pour en garder la trace.

## 6. Poursuivre le travail

À chaque nouvelle histoire, nouveau LoRA ou traitement long :

1. **Mesurer** : lancer `mesure_energie.py echantillonner` pendant le traitement, noter l'énergie dans le journal de la piste.
2. **Conserver les durées** : garder `resultats.json`, `bilan.json` et les journaux d'appels ; ne pas écraser une image de même nom sans conserver le journal de relance (sinon l'image n'est plus comptée).
3. **Déclarer les nouveautés dans `bilan_energie.py`** : un nouveau LoRA dans `LORAS`, une nouvelle histoire dans la liste des scènes (et sa provenance), les essais écartés dans `ECARTES`, les dossiers d'essais dans `ESSAIS_H1` (à renommer en liste générale d'essais préparatoires).
4. **Relancer** `python bilan_energie.py`, puis le PDF et le carrousel.
5. **Revérifier les prix et facteurs** (la date de relevé figure dans le tableau des sources) : tarif de l'électricité, prix du cloud, facteur d'émission, taux de change.

## 7. Point énergétique final

À la fin du projet : régénérer le rapport avec tous les LoRA et toutes les histoires ; refaire les mesures de puissance qui reposent sur une hypothèse (CPU et reste du PC : wattmètre de prise ou HWiNFO) ; mettre à jour le prix de la machine, le rythme d'usage réel pour l'amortissement et le nombre d'images retenues par LoRA ; comparer avec le bilan intermédiaire (archives datées) ; republier l'édition publique et le carrousel.

## 8. Dupliquer sur un autre projet ou une autre machine

Reprendre `bilan_energie.py`, `mesure_energie.py`, `bilan_pdf.py` et `carrousel.py` ; adapter : les constantes en tête (puissances, tarifs, facteurs d'émission, prix de la machine), les dictionnaires des entraînements et des histoires, les chemins des journaux, la liste de remplacements de l'édition publique (`REMPLACEMENTS_PUBLIC`) et la liste des termes interdits (`INTERDITS_PUBLIC`), qui font refuser la publication si un nom personnel subsiste. Aucune dépendance externe (Chrome pour les PDF, `nvidia-smi` pour le GPU).

## 9. Limites à garder en tête

Voir la section « Limites et incertitudes » du rapport : minimum côté images supprimées, puissance du CPU estimée, hypothèses du cloud, entraînement des modèles et fabrication du matériel non comptés.
