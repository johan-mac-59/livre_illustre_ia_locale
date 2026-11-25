# Bilan énergie, coût et CO2 du travail local (2026-11-24)

Généré par `python bilan_energie.py`. Local : durées réelles x puissance (GPU 201 W mesuré à pleine charge, CPU estimé 27 W, soit 228 W ; le reste du PC est ignoré, décision de l'auteur). Électricité : 0.2001 €/kWh (tarif réglementé Base TTC), CO2 France 52 g/kWh. Cloud : hypothèses en tête de `bilan_energie.py`.

## À citer, non calculable : entraînement des modèles et fabrication du matériel

Ce bilan ne compte **pas** l'énergie ni les émissions de CO2 de l'entraînement des modèles utilisés : modèles cloud (Claude, modèles de fal.ai) et modèles ouverts que l'auteur fait tourner en local (Qwen-Image 2.1 et 2512, Flux Klein, Z-Image, Qwen3.6 et 3.8, Gemma 4, Mistral, minicpm-v...). Cet entraînement est colossal, mais ses chiffres ne sont pas publiés de façon fiable pour la plupart de ces modèles, et il est partagé entre tous leurs utilisateurs : il n'est pas calculable pour cet usage. Il est identique dans les deux scénarios, car le local utilise des modèles ouverts entraînés par de grands acteurs, le cloud des modèles entraînés par d'autres : ce bilan compare donc des **usages**, pas des cycles de vie complets. Seul l'entraînement de ses 4 LoRA, réalisés par l'auteur, est compté (décision de l'auteur, 2026-11-24).

De même, le **CO2 de fabrication du matériel** (le PC et le GPU de l'auteur, les serveurs et GPU des datacenters, les réseaux) ne peut pas être estimé de façon fiable : aucune donnée propre à ces machines, partage entre leurs usages et durée de vie inconnue. Il n'est compté ni côté local ni côté cloud, il existe dans les deux cas et il est loin d'être nul : l'amortissement en euros de la section 9 ne le mesure pas. À citer à part, non chiffré.

## 1. Chaque LoRA : entraînement, dessins du jeu, tests

| LoRA | Entraînement (pas, h) | Dessins générés pour le jeu (gardés) | Tests (images) | Énergie totale locale (Wh) | € | kg CO2 |
|---|---|---|---|---|---|---|
| personnage 1 | 3300 pas, 8.0 h = 1888 Wh | 192 (33) = 516 Wh | 56 = 398 Wh | 2802 | 0.56 | 0.15 |
| personnage 2 | 3700 pas, 8.8 h = 2080 Wh | 141 (37) = 395 Wh | 56 = 399 Wh | 2873 | 0.57 | 0.15 |
| personnage 3 | 3500 pas, 8.4 h = 1970 Wh | 126 (35) = 315 Wh | 70 = 499 Wh | 2784 | 0.56 | 0.14 |
| personnage 4 | 5000 pas, 11.9 h = 2808 Wh | 150 (38) = 369 Wh | 98 = 695 Wh | 3872 | 0.77 | 0.20 |
| **Total retenu** | | | | **12331** | **2.47** | **0.64** |

Essais écartés (entraînements remplacés, jeux erronés) :

- personnage 1 v1 (2000 pas) : 1760 Wh (4.8 h d'entraînement, 112 images de test)
- personnage 4 v1 (4700 pas) : 3031 Wh (11.2 h d'entraînement, 56 images de test)
- personnage 2, jeu erroné : 398 Wh (0.0 h d'entraînement, 56 images de test)
- essais d'images préparatoires de l'histoire 1 : 85 Wh (30 images)

Sous-total écarté : 5273 Wh, 1.06 €, 0.27 kg CO2. Les essais d'anneau, d'yeux et les échecs d'entraînement (coupure de courant, run du personnage 2 raté) ne sont pas comptés : le total local est donc un minimum.

## 2. Images des livres : dessin depuis une photo (sans LoRA) et dessin par LoRA

| Histoire | Images générées (candidats, 3 graines) | Durée | Énergie (Wh) | Images utilisées | Wh par image générée | Wh par image utilisée |
|---|---|---|---|---|---|---|
| histoire 1 | 74 | 1.21 h | 276 | 8 | 3.7 | 34.4 |
| histoire 2 | 75 | 2.96 h | 675 | 10 | 9.0 | 67.5 |
| histoire 3 | 66 | 1.27 h | 290 | 19 | 4.4 | 15.3 |
| **Total** | 215 | 5.44 h | **1240** | 37 | 5.8 | 33.5 |

Mesure directe de l'histoire 03 (échantillonneur, 60 images) : 3,5 Wh par image, ce qui confirme le calcul par les durées.

### Coût d'une image : sans LoRA, avec LoRA

| Cas | Wh par image | € | g CO2 (France) |
|---|---|---|---|
| Dessin depuis une photo, sans LoRA, par image UTILISÉE (candidats compris) | 33.5 | 0.0067 | 1.7 |
| Dessin depuis une photo, par image générée | 5.8 | 0.0012 | 0.3 |
| Image par LoRA, coût marginal (une génération avec le modèle fusionné) | 6.0 | 0.0012 | 0.3 |
| Image par LoRA, coût amorti (les 4 LoRA retenus ÷ 3 images de livre qui en viennent) | 4110 | 0.82 | 214 |

| LoRA | Dessins générés / gardés pour le jeu | Énergie totale (Wh) | Images de livre issues du LoRA | Wh par image de livre |
|---|---|---|---|---|
| personnage 1 | 192 / 33 | 2802 | 1 | 2802 |
| personnage 2 | 141 / 37 | 2873 | 1 | 2873 |
| personnage 3 | 126 / 35 | 2784 | 1 | 2784 |
| personnage 4 | 150 / 38 | 3872 | 1 | 3872 |

Avec une seule image de livre par LoRA, une image par LoRA coûte 713 fois plus d'énergie qu'un dessin depuis photo, alors que leur coût marginal est le même (6.0 contre 5.8 Wh). Le LoRA ne se justifie donc pas par l'énergie mais par la cohérence du personnage ; son coût fixe (3083 Wh en moyenne) ne devient négligeable qu'avec plusieurs centaines d'images du même personnage (il en vaut 534 dessins depuis photo).

## 3. Texte (modèles Ollama locaux) : production et mise au point

La **mise au point** regroupe les bancs de modèles et de prompts, les essais de fidélité de l'histoire 01 et les anciens runs de livre ; la **production** regroupe le texte réellement livré (histoires 02 et 03, texte final de l'histoire 01).

| | Appels | Calcul (h) | Tokens entrée / sortie (M) | Énergie (Wh) | € | kg CO2 | Cloud Sonnet 5 ($) |
|---|---|---|---|---|---|---|---|
| production | 399 | 1.4 | 0.16 / 0.05 | 94 | 0.02 | 0.005 | 0.8 |
| mise au point | 4733 | 19.9 | 1.48 / 0.49 | 1297 | 0.26 | 0.067 | 7.8 |

65 W de moyenne mesurée sur le texte de l'histoire 03 ; 3,5 caractères par token ; tokens de réflexion non comptés ; appels sans journal absents.

## 4. Total local : mise au point (coût fixe) contre usage (production)

| Poste | Wh | € | kg CO2 |
|---|---|---|---|
| **MISE AU POINT** |  |  |  |
| LoRA retenus (entraînement, jeux, tests) | 12331 | 2.47 | 0.641 |
| Essais écartés (LoRA remplacés, jeux erronés, essais d'images de l'histoire 1) | 5273 | 1.06 | 0.274 |
| Bancs et essais de texte | 1297 | 0.26 | 0.067 |
| Sous-total mise au point | 18901 | 3.78 | 0.983 |
| **USAGE** |  |  |  |
| Images des 3 histoires (candidats compris) | 1240 | 0.25 | 0.064 |
| Texte livré | 94 | 0.02 | 0.005 |
| Sous-total usage | 1334 | 0.27 | 0.069 |
| **Total** | **20235** (20.2 kWh) | **4.05** | **1.05** |

Usage : 445 Wh (0.089 €, 23 g CO2) par histoire en moyenne. La mise au point (18.9 kWh) représente 93 % du total : c'est un coût unique qui se dilue sur les histoires suivantes, alors que l'usage seul est faible.

## 5. Même travail dans le cloud (hypothèses)

- **Argent** : entraînement fal.ai 0.00095 $/pas ; dessins depuis photo 0.03 $/Mpx ; images LoRA 0.035 $/Mpx ; texte Claude Sonnet 5 2.0/10.0 $ par million de tokens (entrée/sortie). Taux 1,11 $ pour 1 € (moyenne de novembre 2026, Banque de France). Hors forfait de Claude Code, qui orchestre et écrit les scripts dans les deux cas.

| | Local (€ TTC) | Cloud ($ HT) | Cloud (€ HT) | Cloud (€ TTC) |
|---|---|---|---|---|
| Mise au point | 3.78 | 68 | 61 | 73 |
| Usage (3 histoires) | 0.27 | 8 | 7 | 8 |
| **Total** | **4.05** | **75** | **68** |

Détail de la mise au point, entraînement séparé de l'usage (LoRA retenus et écartés confondus) :

| Poste | Local (Wh) | Local (€) | Cloud (Wh, 8x à 4x) | Cloud ($) |
|---|---|---|---|---|
| LoRA, entraînement | 12500 | 2.50 | 5583 à 11165 | 21.1 |
| LoRA, dessins du jeu | 1594 | 0.32 | 734 à 1468 | 19.2 |
| LoRA, tests | 3425 | 0.69 | 1577 à 3153 | 18.5 |
| essais d'images de l'histoire 1 | 85 | 0.02 | 39 à 78 | 0.9 |
| Texte, bancs et essais | 1297 | 0.26 | 1136 à 1609 | 7.8 |
| **Usage** : images des livres | 1240 | 0.25 | 571 à 1142 | 6.8 |
| **Usage** : texte livré | 94 | 0.02 | 96 à 136 | 0.8 |

- **Scénario B, location d'un GPU** (RunPod, H100 SXM à 3.99 $/h, facturé à la seconde ; mêmes outils qu'en local, H100 4 à 8 fois plus rapide) : mise au point 41 à 81 € TTC (images et LoRA, hors texte), usage 3 à 6 € TTC. Hors stockage des modèles (environ 340 Go, facturé à part) et temps de démarrage, qui augmenteraient ce chiffre.
- Les deux scénarios (API par image chez fal.ai, location de GPU) donnent un ordre de grandeur voisin pour la mise au point : 49 à 90 € TTC, contre 3.78 € en local.

- **Énergie** (images et entraînements ; texte cloud : 0,24 à 0,34 Wh par requête, sources en bas, probablement sous-estimé car nos requêtes sont plus longues qu'une requête médiane) : un H100 de 700 W x PUE 1.2 est supposé 4 à 8 fois plus rapide que la RTX 5070.

| Énergie (Wh) | Local | Cloud, 8 fois plus rapide | Cloud, 4 fois plus rapide |
|---|---|---|---|
| Mise au point (LoRA, essais écartés ; sans texte) | 17605 | 7932 | 15865 |
| Usage (images des livres ; sans texte) | 1240 | 571 | 1142 |
| CO2 total (kg) : France en local (52 g/kWh), États-Unis dans le cloud (384 g/kWh, lieu supposé) | 0.98 | 3.27 | 6.53 |
| CO2 du texte (kg) : bancs et essais / texte livré | 0.067 / 0.005 | 0.436 à 0.618 / 0.037 à 0.052 | même fourchette (0,24 à 0,34 Wh par requête) |

Pour le texte cloud, Google publie 0,03 g CO2e par requête médiane avec une comptabilité « marché » (électricité renouvelable achetée, réseau net à 94 g/kWh en 2024) ; ici le texte est compté comme le reste du cloud, au réseau américain moyen (384 g/kWh), soit 0.09 à 0.13 g par requête : l'écart avec les 0,03 g de Google vient uniquement de la méthode de comptabilité.

## 6. Scénario sans LoRA : toutes les images viennent de photos

Hypothèse : les 3 images de livre dessinées par un LoRA auraient été tirées de photos, comme les 34 autres : aucun entraînement, aucun jeu de dessins, aucun test de LoRA, aucun essai écarté. Chaque image de remplacement coûte comme une image moyenne des livres (33.5 Wh avec ses candidats, soit 5.8 dessins générés par image utilisée). Le texte reste identique (bancs et production). Chiffre légèrement surestimé, car les images de LoRA déjà générées sont peut-être comptées dans les images des livres.

| | Local | Cloud A : API fal.ai | Cloud B : location de GPU |
|---|---|---|---|
| **Avec LoRA** (bilan complet) : € TTC | 4.05 | 81 | 53 à 97 |
| **Sans LoRA** : € TTC | 0.56 | 18 | 13 à 16 |
| Sans LoRA : énergie (kWh) | 2.82 | 1.89 à 3.06 | idem A |
| Sans LoRA : CO2 (kg) | 0.15 (France) | 0.73 à 1.17 (États-Unis) | idem A |

Sans LoRA, le local coûte 0.56 € au lieu de 4.05 € (86 % d'énergie en moins) ; le cloud passe de 81 € à 18 € (API) : les LoRA représentent 86 % de l'énergie du bilan pour 3 images de livre sur 37. Ils se justifient par la cohérence des personnages et par le choix de ne pas dépendre de photos, pas par le coût.

## 7. Transfert de données : télécharger les modèles en local, contre l'usage du cloud

- **Local** : environ 337 Go de modèles présents (ComfyUI 114 Go hors fusions + 72 Go d'encodeurs + 6 Go divers, Ollama 145 Go), téléchargés une fois ; minimum, car des modèles supprimés (Mistral Small 4, 58 Go, etc.) ont aussi été téléchargés. Les fusions (82 Go) sont calculées en local, non téléchargées.
- **Cloud** : environ 8 Go à transférer pour le même travail (photos et jeux envoyés, 1358 images reçues à 2 Mo, 4 LoRA récupérés), les modèles restant chez le fournisseur.
- Intensité du transfert : **central 0.02 kWh/Go** (Arcep 2026, données 2024, réseau fixe français, hypothèse de 200 Go par mois et par abonnement), haut 0.05 (avec les box), bas 0.0013 (extrapolation d'Aslan 2015). Le coût d'un transfert = Go transférés x kWh par Go, puis x g de CO2 par kWh.

| Intensité | Local, téléchargement (kWh) | Cloud, transferts (kWh) | CO2 local (kg, France) | CO2 cloud (kg, France) |
|---|---|---|---|---|
| bas (0.0013 kWh/Go) | 0.44 | 0.01 | 0.023 | 0.001 |
| central (0.02 kWh/Go) | 6.74 | 0.16 | 0.350 | 0.008 |
| haut (0.05 kWh/Go) | 16.85 | 0.40 | 0.876 | 0.021 |

Le téléchargement des modèles est un coût unique, amorti sur tous les livres futurs ; il est à comparer au total local ci-dessus. Le cloud supprime ce coût mais le répète à chaque usage, en bien plus petit.

## 8. Totaux avec les transferts de données (énergie et CO2)

Les prompts, les photos envoyées, les images reçues ou affichées par internet et les modèles téléchargés sont comptés comme le reste : 337 Go pour le local (modèles, une fois), 8 Go pour le cloud (1358 images reçues à 2 Mo, photos et jeux envoyés, 4 LoRA récupérés, texte). Réseau compté au facteur français (52 g/kWh), énergie du réseau seulement (aucun euro : l'abonnement internet est forfaitaire). Le trafic de l'orchestration par Claude Code est identique dans les deux scénarios et exclu.

| Intensité du transfert | Local : énergie totale (kWh) | Local : CO2 (kg) | Cloud : énergie totale (kWh) | Cloud : CO2 (kg) |
|---|---|---|---|---|
| bas (0.0013 kWh/Go) | 20.7 | 1.07 | 9.7 à 18.8 | 3.74 à 7.20 |
| central (0.02 kWh/Go) | 27.0 | 1.40 | 9.9 à 18.9 | 3.75 à 7.21 |
| haut (0.05 kWh/Go) | 37.1 | 1.93 | 10.1 à 19.1 | 3.76 à 7.22 |

Le transfert pèse peu dans le cloud (quelques Go). En local, le téléchargement des modèles est un coût unique qui devient notable avec l'intensité haute (0,05 kWh/Go), mais il sert à tous les livres futurs.

## 9. Amortissement de la machine complète (1357 €)

Le matériel est compté 1357 € (prix réels payés par l'auteur, parfois d'occasion récente), **composant par composant** : chacun a sa propre usure et sa propre obsolescence, donc sa propre durée de vie. On amortit chaque composant linéairement sur sa durée, puis on impute au projet la part correspondant à ses heures de calcul. Le projet totalise **102 h de calcul** (images, LoRA, essais, texte, nuits d'entraînement comprises) réparties sur 19 jours (du 6 au 24 novembre 2026), soit 5.4 h par jour en moyenne.

Le coût par heure de calcul dépend de la durée de vie de chaque composant et du rythme d'usage de la machine sur cette durée (non connu : elle sert aussi à autre chose, et le projet va ralentir une fois les livres faits). Référence : 4 h de calcul par jour.

| Composant | Prix | Durée comptable / garantie constructeur (référence) / estimation ambitieuse | Coût par heure de calcul (référence) | Part du projet (référence) |
|---|---|---|---|---|
| Carte graphique (RTX 5070) | 400 € | 3 / 3 / 8 ans | 0.091 €/h | 9.3 € |
| Processeur (Core Ultra 7 265K) | 290 € | 3 / 3 / 8 ans | 0.066 €/h | 6.8 € |
| Mémoire vive (Corsair Vengeance 2x32 Go DDR5) | 217 € | 3 / 3 / 10 ans | 0.050 €/h | 5.1 € |
| Carte mère (Gigabyte B860 AORUS ELITE WIFI7 ICE) | 160 € | 3 / 3 / 8 ans | 0.037 €/h | 3.7 € |
| Boîtier (Corsair 4000D) | 100 € | 3 / 2 / 8 ans | 0.034 €/h | 3.5 € |
| Alimentation (MSI 850 W Gold) | 90 € | 3 / 10 / 10 ans | 0.006 €/h | 0.6 € |
| SSD NVMe (Samsung 990 PRO 1 To) | 100 € | 3 / 5 / 8 ans | 0.014 €/h | 1.4 € |
| **Total** | **1357 €** | | **0.298 €/h** | **30.5 €** |

Fourchette selon les durées de vie et le rythme d'usage (même rythme que le projet, 4 h par jour, 2 h par jour) :

| Rythme de calcul de la machine | Durée comptable (3 ans partout) | Garantie constructeur (référence) | Estimation ambitieuse (haut des guides) |
|---|---|---|---|
| même rythme que le projet (5.4 h/j) | 0.23 €/h, soit 24 € pour le projet | 0.22 €/h, soit 23 € pour le projet | 0.08 €/h, soit 8 € pour le projet |
| 4 h par jour (4.0 h/j) | 0.31 €/h, soit 32 € pour le projet | 0.30 €/h, soit 30 € pour le projet | 0.11 €/h, soit 11 € pour le projet |
| 2 h par jour (2.0 h/j) | 0.62 €/h, soit 63 € pour le projet | 0.60 €/h, soit 61 € pour le projet | 0.22 €/h, soit 23 € pour le projet |

**Valeur de référence retenue : garantie constructeur de chaque composant, 4 h de calcul par jour, soit 30 € pour le projet** (fourchette 8 à 63 €). **Estimation ambitieuse (durées de vie réelles probables, haut des guides) : 11 € pour le projet.** En ajoutant l'amortissement à l'électricité (4.05 € TTC), le local coûte **35 € TTC** contre 81 € (cloud A, API) et 53 à 97 € (cloud B). L'amortissement pèse donc bien plus que l'électricité dans le coût du local (88 % du total), et le local reste moins cher que le cloud sur ce projet.

**D'où viennent les durées (chacune a une source, aucune n'est estimée au jugé).** *Garantie constructeur* (référence) : durée que le constructeur s'engage à couvrir, donc une **borne basse** de la vie réelle, non la vie elle-même. Carte graphique : 3 ans chez les partenaires de la RTX 5070 (pages de revendeurs : ASUS, MSI, PNY, Gigabyte). Processeur : 3 ans, politique de garantie Intel des processeurs en boîte. Carte mère : 3 ans (un seul revendeur, à confirmer chez Gigabyte). SSD Samsung 990 PRO 1 To : 5 ans ou 600 To écrits (fiche technique Samsung) ; l'usage de ce projet reste très loin de 600 To. Alimentation MSI 850 W Gold : 10 ans pour la gamme MAG A850GL (modèle exact à confirmer). Boîtier Corsair 4000D : 2 ans pour la gamme. Mémoire Corsair : garantie à vie limitée, donc sans durée chiffrée : on retient les 3 ans comptables. *Durée comptable* : 3 ans pour un ordinateur, convention donnée par des cabinets comptables (la doctrine fiscale officielle n'a pas été vérifiée). *Estimation ambitieuse* (vie réelle probable, sources plus faibles : guides grand public, pas d'étude) : carte graphique 8 ans (haut de la fourchette de 5 à 8 ans de Digital Trends) ; mémoire 10 ans (Digital Trends et BGR : on la remplace pour obsolescence bien avant sa panne) ; alimentation 10 ans (haut de la fourchette de 5 à 10 ans de BGR, aussi sa garantie) ; processeur, carte mère, boîtier et SSD 8 ans, haut de la fourchette de 3 à 8 ans que HP donne pour un ordinateur de bureau entier (aucune source propre à ces composants). Pour le SSD, l'usure ne limite pas la durée : 600 To en 5 ans correspondent à environ 330 Go écrits par jour, très au-delà du projet ; c'est l'obsolescence qui compte. Une seule source, peu fiable, annonce des SSD qui dépassent 20 fois leur endurance : écartée. Aucune étude solide ne donne la durée de vie d'une carte grand public sous charge d'entraînement ; une durée de 1 à 3 ans attribuée à un architecte de Google pour les GPU de datacenter n'est pas vérifiée. L'obsolescence compte autant que l'usure : 12 Go de VRAM seront dépassés avant que la carte soit hors d'usage, ce qui plaide pour ne pas allonger la durée de la carte graphique.

**Ce que ça change dans la comparaison.** Les chiffres sont à prendre comme un ordre de grandeur : le coût du local dépend surtout de l'usage futur du matériel. Plus le GPU sert (autres projets, livres suivants), plus le coût par heure baisse : avec les durées de référence, 0.30 €/h à 4 h par jour, 0.60 €/h à 2 h par jour. Pour comparer, un H100 loué coûte environ 4.3 € TTC l'heure, soit 0.54 à 1.08 € par heure de calcul équivalente à la carte de l'auteur (H100 4 à 8 fois plus rapide). Le matériel est déjà acheté : son coût est engagé quel que soit l'usage, alors que le cloud ne se paie qu'à l'usage ; cette asymétrie joue en faveur du cloud si le projet restait ponctuel.

## Souveraineté et confidentialité des données (hors calcul)

Cette partie n'entre dans aucun chiffre ci-dessus (décision de l'auteur : l'avantage du local en confidentialité est noté à part), mais elle compte autant que le coût pour ce projet. Les données traitées sont des **photos personnelles de famille, dont des enfants**, des **vidéos de famille**, des **textes de souvenirs réels** (histoires vécues, noms, lieux, relations) et des **visages appris par des LoRA** (personnage 1, personnage 2, personnage 3, personnage 4).

| Donnée | Local (la pratique du projet) | Cloud : envoi nécessaire pour refaire le même travail |
|---|---|---|
| Photos réelles et images de vidéos | Restent dans le dossier privé des données (hors git) et ne passent que par des modèles locaux (ComfyUI, Ollama). Règle du projet : Claude Code ne les visualise jamais ; il écrit le code, les modèles locaux les regardent. | Chaque photo serait envoyée au fournisseur pour être transformée en dessin (fal.ai ou autre), soit plusieurs centaines de photos dans nos essais. |
| Visages des enfants et des adultes | Les LoRA sont entraînés et stockés en local (poids de quelques centaines de Mo, fusions d'environ 20 Go) ; personne d'autre n'y a accès. | Un entraînement cloud exige d'envoyer le jeu d'images du visage (33 à 38 dessins par personne, tirés de photos) et de récupérer le LoRA ; le fournisseur voit un jeu complet de visages identifiables d'enfants. |
| Textes des histoires réelles | Traités par des modèles locaux seulement (rôles correcteur, adaptateur, relecteur) ; les textes ne sont pas versionnés. | Le texte des souvenirs (prénoms, lieux, événements familiaux) serait envoyé à un modèle de texte hébergé, à chaque essai de prompt et de relecture. |
| Prompts et journaux | Restent dans `logs/` et `sorties/` (hors git). | Prompts, images et résultats transitent et peuvent être conservés par le fournisseur selon ses conditions. |
| Où sont les données | Sur la machine de l'auteur, en France. | Chez des fournisseurs dont l'hébergement, la conservation et l'usage pour l'amélioration des modèles dépendent de leurs conditions, que ce bilan n'a pas vérifiées ; le lieu des datacenters n'est pas connu (hypothèse États-Unis pour le CO2). |

**Pourquoi c'est sensible.** Les images d'enfants et les visages sont des données personnelles ; un envoi à un tiers hors de la maîtrise de l'auteur est un acte qu'on ne peut pas défaire (le contenu peut être copié, journalisé ou conservé même après suppression). Ce bilan ne donne pas d'avis juridique (RGPD, droit à l'image des mineurs) : à faire valider si le livre est un jour diffusé. Au contraire, l'usage strictement familial en local limite l'exposition.

**Souveraineté** (maîtrise de ses outils et de son travail) :

- **Dépendance et prix** : en local, les modèles et les LoRA appartiennent à l'utilisateur et sont reproductibles à l'identique ; dans le cloud, les prix et les modèles changent hors de la main de l'utilisateur. Exemples relevés en novembre 2026 : RunPod a relevé ses tarifs en octobre (H100 SXM de 3,49 à 3,99 $/h) ; Anthropic avait annoncé de passer Claude Sonnet 5 de 2 $/10 $ à 3 $/15 $ puis y a renoncé ; OpenAI retire gpt-image-1 le 23 octobre et gpt-image-1.5 le 1er décembre 2026 (sources en bas). Un livre refait dans un an avec les mêmes modèles n'est garanti que s'ils sont gardés en local.
- **Disponibilité** : le local fonctionne hors connexion, une fois les modèles téléchargés ; le cloud dépend de la connexion et du fournisseur.
- **Licences** : certains modèles utilisés sont à licence de recherche ou non commerciale (Qwen-Image 2.1, Flux Klein 9B) ; l'usage familial local est cohérent avec ces licences, alors que le passage par un service commercial et une diffusion du livre demanderaient de vérifier les conditions (point déjà noté dans le projet).
- **Contrepartie du local** : l'utilisateur est responsable de la sécurité de sa machine et de ses sauvegardes (les LoRA et le dossier privé des données ne sont pas versionnés), et il porte le coût matériel (GPU de 12 Go, consommation, chaleur).
- **Le cloud n'est pas écarté pour tout** : le texte de production d'une histoire réelle pourrait rester local tandis qu'un calcul sans donnée personnelle (par exemple un banc de modèles sur des textes fictifs) irait dans le cloud.

## Limites et incertitudes

Chaque limite indique son effet sur les résultats : **sous-estime** (le vrai chiffre est plus haut), **surestime** (plus bas) ou **incertain** (dans les deux sens). Les chiffres du bilan sont donc des ordres de grandeur, avec un biais global vers le bas côté local (voir la fin de cette section).

### Mesures et puissances (local)

- **Trois puissances sont mesurées** : GPU en génération d'images, 201 W (nvidia-smi, phases au-dessus de 90 % d'utilisation, histoire 03) ; texte, 65 W de moyenne (34 min de l'histoire 03) ; GPU en entraînement, 208 W (essai du 2026-11-24, voir ci-dessous). Tout le reste en découle par les durées enregistrées. *Incertain.*
- **Puissance de l'entraînement des LoRA : mesurée sur un essai de 40 pas** (musubi-tuner, jeu du personnage 2, mêmes réglages : 45 blocs en RAM, 1024 x 1024, 8,63 s par pas, comme les entraînements d'origine), échantillonnage chaque seconde pendant 286 s de pas réels : **208 W en moyenne pour le GPU** (médiane 220 W, maximum 223 W, minimum 51 W), utilisation moyenne de 94 %, CPU 10 %. Le GPU descend bien parfois en charge (24 % du temps sous 90 % d'utilisation, pendant les échanges entre RAM et GPU) mais la puissance reste sous 150 W pendant 0,3 % du temps seulement : la moyenne est donc proche de la pleine charge. Cette valeur remplace les 201 W pour les durées d'entraînement. Puissance nominale de la carte : 250 W, jamais atteinte pendant l'essai. Limites : 40 pas seulement (5 minutes), un seul jeu d'images, une carte thermiquement froide au départ ; la puissance peut dériver d'un point ou deux sur 8 heures. *Faible incertitude.*
- **La puissance du CPU est estimée** par l'utilisation (15 W au repos, 125 W à pleine charge d'après `mesure_energie.py`) et appliquée avec l'utilisation de 11 % relevée pendant les images, y compris à l'entraînement et au texte, où elle peut être différente. Ni compteur de puissance ni HWiNFO. *Incertain.*
- **Le reste du PC est ignoré** (mémoire, SSD, carte mère, ventilateurs, pertes de l'alimentation, écran) : décision de l'auteur, d'après l'hypothèse que ce poste est mineur. Un wattmètre de prise le mesurerait. *Sous-estime le local.*
- **Les durées viennent des fichiers de résultats.** Les temps d'attente du GPU entre deux tâches (chargements de modèles, reprises, contrôles, veille), les fusions de LoRA (environ 1 minute chacune) et les caches d'entraînement (environ 80 secondes par LoRA) ne sont pas comptés. Sur l'histoire 03, la mesure continue donne 267 Wh pour 104 min, contre une somme des images plus basse. *Sous-estime le local.*
- **Durée d'entraînement du personnage 1 estimée** (3 300 pas x 8,76 s, vitesse relevée dans le journal) et du personnage 4 v2 en partie (3 800 pas x 8,6 s), car `bilan.json` ne la contient pas. *Incertain, faible effet.*
- **Les contrôles automatiques des images** (qwen3.6 en vision) ne sont comptés qu'à 17 s par image de test de LoRA (estimation) et dans les journaux Ollama quand ils existent. *Sous-estime le local.*

### Comptage des images et du texte

- **Seules les images présentes sur le disque ou dans un journal sont comptées.** Les images générées puis supprimées, ou écrasées par une relance de même nom, ne laissent pas de trace, sauf pour l'histoire 1 (21 images retrouvées dans les journaux de relance). Pour les histoires 2 et 3, aucun journal de relance n'existe. *Sous-estime, en local comme dans le cloud.*
- **Non comptés** : les essais d'anneau et d'yeux du personnage 4, les échecs d'entraînement (coupure de courant au pas 494 du premier LoRA du personnage 1, run du personnage 2 raté). *Sous-estime.*
- **8 images de l'histoire 2 sans durée enregistrée** sont comptées à la durée moyenne des autres. *Incertain, faible effet.*
- **Les images « utilisées » (37) sont comptées d'après les fichiers de provenance** : une image propre à un enfant compte une fois, et les éléments d'une composition ne comptent pas. Le LoRA n'a servi que pour 3 images de livre, donc tout coût par image de LoRA est très sensible à ce petit nombre. *Incertain.*
- **Texte** : seuls les appels journalisés sont comptés (5 132), le classement en production ou mise au point repose sur le dossier du journal, les tokens de réflexion des modèles ne sont pas comptés, et les tokens sont estimés à 3,5 caractères. *Sous-estime côté tokens, incertain côté classement.*
- **Scénario sans LoRA** : les 3 images de remplacement sont comptées au coût moyen d'une image des livres, mais certaines images de LoRA sont peut-être déjà comptées dans les images des livres. Il suppose aussi que des photos adaptées auraient existé pour ces scènes. *Surestime légèrement.*

### Hypothèses du cloud

- **Même déroulé supposé** (décision de l'auteur) : le cloud refait les mêmes images, les mêmes pas, les mêmes appels de texte. En vrai, un service cloud pourrait demander moins ou plus d'essais. *Incertain.*
- **Scénario A (API fal.ai)** : les tarifs de fal.ai ne correspondent pas exactement à nos modèles (Qwen-Image 2.1 en édition, Klein, Z-Image) ; le tarif d'entraînement LoRA (0,00095 $ par pas) n'a pas pu être confirmé sur la page, un article plus ancien donne 0,002 $ ; les images sont comptées à 1,05 mégapixel ; le prix des images avec LoRA vient d'un résultat de recherche. *Incertain, fourchette 21 à 44 $ pour l'entraînement.*
- **Scénario B (location d'un GPU)** : prix RunPod relevés dans des résumés de recherche, qui diffèrent selon les pages (de 2,69 à 4,39 $/h pour un H100) ; sans le stockage des modèles (environ 340 Go), le temps de démarrage ni l'installation. *Sous-estime ce scénario.*
- **Accélération du H100 supposée 4 à 8 fois** la RTX 5070, sans mesure ; puissance de 700 W et PUE de 1,2 non sourcés. L'énergie cloud en dépend directement. *Incertain.*
- **Lieu du datacenter supposé aux États-Unis** (384 g/kWh, moyenne 2024) : ni fal.ai ni Anthropic ne le précisent ; Google publie 0,03 g par requête avec une comptabilité « marché » qui donnerait un CO2 bien plus bas. *Incertain, grand effet sur le CO2.*
- **Énergie du texte cloud** : 0,24 à 0,34 Wh par requête médiane ; nos requêtes sont plus longues, et aucune valeur n'existe pour Claude. *Sous-estime.*
- **TVA de 20 %** ajoutée aux prix HT : à vérifier sur une facture. **Taux de change** : moyenne de 16 jours de novembre 2026 (1,11). *Incertain, faible effet.*

### Électricité, CO2 et transferts

- **Tarif de 0,2001 €/kWh** : tarif réglementé Base TTC, l'abonnement n'est pas compté, ni les heures creuses. *Faible effet.*
- **CO2 de la France de 52 g/kWh** : moyenne annuelle 2024 (Banque de France d'après la Base Carbone, valeur à confirmer dans la Base Empreinte), pas un facteur horaire ; la nuit, le réseau français est en général moins carboné. *Incertain.*
- **Transferts** : 337 Go de modèles est un minimum (des modèles supprimés avaient aussi été téléchargés) ; 2 Mo par image reçue est une estimation ; l'intensité de 0,02 kWh/Go vient de la page de l'Arcep (le PDF n'a pas pu être lu, donc le périmètre exact, box, réseau de cœur et transit international, n'est pas confirmé), fondée sur l'hypothèse de 200 Go par mois ; les données du cloud viennent en partie de l'étranger sans valeur plus récente. Le trafic de l'orchestration par Claude Code n'est pas compté. *Incertain.*

### Exclusions décidées ou impossibles à calculer

- **Entraînement des modèles eux-mêmes** (cloud et ouverts) : colossal, non calculable (voir le début du rapport). Décision de l'auteur, 2026-11-24.
- **Fabrication du matériel** (le PC et le GPU de l'auteur, serveurs et GPU des datacenters, réseaux) : non calculable, à citer (voir le début du rapport). **Refroidissement de la pièce**, **stockage sur disque**, **impression des livres**, **temps humain** : non comptés.
- **Orchestration par Claude Code** (forfait) : identique dans les deux scénarios, exclue des deux ; la mission de calcul elle-même est chiffrée à part, dans l'annexe en fin de rapport.

### Lecture d'ensemble

La plupart des biais vont dans le même sens : le **local est sous-estimé** (PC entier, attentes du GPU, images supprimées, essais non comptés), le **cloud aussi côté images supprimées et texte**, mais **plus incertain côté CO2** à cause du lieu du datacenter. Les ordres de grandeur sont solides : le local coûte quelques euros TTC contre plusieurs dizaines d'euros dans le cloud, et les deux scénarios cloud (API et location de GPU) tombent dans la même fourchette. Les rapports fins (par exemple 4 contre 6 kWh) ne sont pas fiables. Pour réduire l'incertitude du local, la mesure la plus utile serait un wattmètre de prise sur le PC entier pendant un entraînement.


## Sources

Mesures du projet : `sorties/energie/images_h3.csv` et `texte_h3.csv` (échantillonneur `mesure_energie.py`, GPU par nvidia-smi), `bilan.json` de chaque entraînement, `resultats.json` des bancs, journaux d'appels Ollama.

| Donnée | Valeur utilisée | Source | Fiabilité |
|---|---|---|---|
| Tarif de l'électricité | 0,2001 €/kWh TTC (tarif réglementé Base, 3 et 6 kVA) | [Selectra, nouveaux prix du 1er août 2026](https://selectra.info/energie/actualites/marche/nouveaux-prix-electricite-tarif-bleu-1er-aout-2026), qui reprend la grille d'EDF ; confirmé par plusieurs comparateurs le 2026-11-24 (en vigueur depuis le 1er août 2026, aucune révision depuis) | secondaire ; la date d'effet diffère selon les sources (1er août ou 1er septembre), le tarif de février 2026 était de 0,194 |
| CO2 de l'électricité en France | 52 g/kWh (mix moyen France continentale, 2024) | [Banque de France, méthodologie énergie (juillet 2026)](https://www.banque-france.fr/system/files/2026-07/Methodologie_energie.pdf), d'après la Base Carbone de l'ADEME | secondaire ; à confirmer dans la [Base Empreinte de l'ADEME](https://base-empreinte.ademe.fr) |
| CO2 de l'électricité aux États-Unis | 384 g/kWh (2024) | [Ember, US Electricity 2025](https://ember-energy.org/latest-insights/us-electricity-2025-special-report/insight-4-rising-demand-pushes-up-emissions-slight/) | bonne ; le lieu du datacenter de fal.ai ou d'Anthropic est une hypothèse |
| Taux de change | 1,11 $ pour 1 € : moyenne des 16 cours quotidiens du 2 au 23 novembre 2026 (1,1101), arrondie au centième, choix de l'auteur | [Banque de France, parités quotidiennes](https://www.banque-france.fr/fr/statistiques/taux-et-cours/taux-de-change-parites-quotidiennes-2026-11-23) : pages des 6, 13, 20 et 23 novembre lues ; cours de 1,0939 (23 novembre) à 1,1267 (4 novembre) | officielle, pages lues ; le mois n'est pas fini, la moyenne portera sur 16 jours |
| Entraînement LoRA dans le cloud | 0,00095 $ par pas (minimum 500 pas) | [fal.ai, Qwen Image 2512 Trainer V2](https://fal.ai/models/fal-ai/qwen-image-2512-trainer-v2), tarif relevé dans une recherche du 2026-11-24 | NON CONFIRMÉ : la page répond 404 à la relecture ; un article de fal.ai plus ancien donne 0,002 $ par pas (2 $ pour 1 000 pas), ce qui doublerait environ ce poste (21 $ à 44 $) ; à confirmer sur fal.ai |
| Images dans le cloud | 0,03 $/Mpx en édition (Qwen Image Edit 2511), 0,035 $/Mpx pour Qwen Image 2512 avec LoRA | [fal.ai, Qwen Image Edit 2511](https://fal.ai/models/fal-ai/qwen-image-edit-2511) (page lue, 2026-11-24) ; [fal.ai, Qwen Image 2512 LoRA](https://fal.ai/models/fal-ai/qwen-image-2512/lora) (résultat de recherche) ; base Qwen Image 2512 : [0,02 $/Mpx](https://fal.ai/models/fal-ai/qwen-image-2512) (page lue) | tarif du fournisseur ; pas exactement nos modèles (Qwen-Image 2.1 en édition) ; Runware annonce 0,0122 $ par image pour Edit 2511 ([Runware](https://runware.ai/fal-alternative)) |
| Texte dans le cloud | 2 $ en entrée et 10 $ en sortie par million de tokens (Claude Sonnet 5, et Sonnet 5.5 au même prix) | [Anthropic, tarifs](https://platform.claude.com/docs/en/about-claude/pricing.md) (page lue, 2026-11-24) | officielle ; la page ne porte pas de date, mais précise que le tarif de 3 $ et 15 $ annoncé pour le 1er septembre n'aura pas lieu |
| Énergie d'une requête de texte dans le cloud | 0,24 Wh (Google, mesuré) à 0,34 Wh (OpenAI, déclaré) | [Google, Measuring the environmental impact of delivering AI at Google Scale, arXiv 2508.15734](https://arxiv.org/abs/2508.15734) ; OpenAI : déclaration de juin 2025 rapportée par [Hannah Ritchie](https://hannahritchie.substack.com/p/ai-footprint-august-2025) ; estimation Epoch AI de 0,3 Wh rapportée par [Projet Celsius](https://projetcelsius.com/en/blog/chatgpt-query-energy-consumption/) | Google : mesure de production, article lu (tableau 2) ; OpenAI et Epoch : secondaires. Aucune valeur par token pour Claude |
| Énergie par token, ordre de grandeur | 40 à 60 J par token pour des modèles de 180 à 480 milliards de paramètres sur H100 (non utilisé dans le calcul) | [TokenPowerBench, arXiv 2512.03024](https://arxiv.org/abs/2512.03024) | texte du corps lu, figures illisibles ; ne s'applique pas à nos modèles |
| Énergie d'une image dans le cloud (non utilisé) | de 1,6 à 11 Wh par image selon modèle et GPU | [Bertazzini et al., The Hidden Cost of an Image, arXiv 2506.17016](https://arxiv.org/html/2506.17016v1) ; [Energy Scaling Laws for Diffusion Models, arXiv 2511.17031](https://arxiv.org/html/2511.17031) | écart énorme entre études : le calcul cloud utilise donc le temps de calcul et non ces valeurs |
| Énergie du transfert de données | 0,02 kWh/Go (central), 0,05 (haut), 0,0013 (bas) | [Arcep, Pour un numérique soutenable, édition 2026, données 2024](https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/impact-environnemental/enquete-annuelle-pour-un-numerique-soutenable-edition-2026.html) : 0,02 kWh/Go sur le fixe contre 0,14 sur le mobile, sur la base de 200 Go par mois ; 125 kWh par abonnement fixe et par an, box comprises ; valeur basse extrapolée d'[Aslan et al. 2018](https://econpapers.repec.org/RePEc:bla:inecol:v:22:y:2018:i:4:p:785-798) ; critique de [Guennebaud et Bugeau 2024](https://econpapers.repec.org/RePEc:bla:inecol:v:28:y:2024:i:4:p:996-1008) | page lue ; le PDF n'a pas pu l'être, donc le périmètre exact (box, réseau de cœur, transit international) n'est pas confirmé ; les données du cloud viennent en partie de l'étranger, sans valeur plus récente que celle-ci : elle est appliquée aux deux côtés |
| TVA sur les prix cloud | 20 % ajoutés aux prix affichés hors taxes (choix de l'auteur : tarifs TTC) | aucune page officielle de fal.ai ni d'Anthropic ne donne le traitement de la TVA pour l'API ; les blogs indiquent qu'Anthropic l'ajoute pour les clients européens | hypothèse, à vérifier sur une vraie facture |
| Location d'un GPU (scénario B) | 3,99 $/h pour un H100 SXM à la demande | [RunPod, tarifs](https://www.runpod.io/gpu-cloud/pricing) ; hausse du 12 octobre 2026 relevée par [PricingSaaS](https://pricingsaas.com/companies/runpod/diffs/2026W42) | les pages donnent des valeurs différentes (de 2,69 à 4,39 $/h pour un H100 selon l'offre) ; non relu sur la page |
| Autres hébergeurs d'images (non utilisés dans le calcul, pour comparer) | Replicate de 0,007 à 0,03 $ par image Qwen ; RunComfy 0,022 $ ; Qwen Image Edit Plus 0,031 $ chez fal.ai contre 0,05 $ chez Replicate | [Replicate](https://replicate.com/smkrv/qwen-image), [RunComfy](https://www.runcomfy.com/fr/models/qwen/qwen-image/qwen-image-2512), [comparatif invideo, août 2026](https://invideo.io/blog/ai-image-model-pricing/) | agrégateurs, non vérifiés ; confirment l'ordre de grandeur de 0,02 à 0,05 $ par image |
| Générateurs fermés (non utilisés, pour comparer) | OpenAI gpt-image-1.5 : environ 0,034 $ (qualité moyenne, 1024 x 1024) ; Google Gemini 3.1 Flash Image : environ 0,067 $ pour 1K | [OpenAI, gpt-image-1](https://developers.openai.com/api/docs/models/gpt-image-1) ; [Google, tarifs Gemini API](https://ai.google.dev/gemini-api/docs/pricing) | relevés via agrégateurs ; ces services ne gardent pas la cohérence d'un personnage comme un LoRA |
| Changements de prix et retraits de modèles (souveraineté) | RunPod H100 SXM de 3,49 à 3,99 $/h (octobre 2026) ; Claude Sonnet 5 resté à 2 $ et 10 $ ; gpt-image-1 retiré le 23 octobre et gpt-image-1.5 le 1er décembre 2026 | [PricingSaaS, RunPod](https://pricingsaas.com/companies/runpod/diffs/2026W42) ; [Anthropic, tarifs](https://platform.claude.com/docs/en/about-claude/pricing.md) ; [OpenAI, gpt-image-1](https://developers.openai.com/api/docs/models/gpt-image-1) | RunPod et OpenAI : relevés dans des résumés de recherche, non relus sur les pages ; Anthropic : page lue |
| Durée de vie du matériel | garantie constructeur de chaque composant (2 à 10 ans) en référence, comparée à 3 ans comptables et à une estimation ambitieuse (3 à 10 ans) | [Darty, choisir sa carte graphique](https://www.darty.com/darty-et-vous/high-tech/informatique/pc-mac/carte-graphique-comment-bien-choisir) : plus de 7 ans avec entretien ; [PCComponentes](https://www.pccomponentes.fr/blog/carte-graphique-doccasion) : les GPU modernes sont conçus pour tourner des années, l'usure vient surtout de la chaleur et du manque d'entretien ; [Tom's Hardware](https://www.tomshardware.com/pc-components/gpus/datacenter-gpu-service-life-can-be-surprisingly-short-only-one-to-three-years-is-expected-according-to-unnamed-google-architect) : 1 à 3 ans en datacenter, source anonyme non vérifiée ; [Meta et Oak Ridge, arXiv 2503.11901](https://arxiv.org/pdf/2503.11901) : mesures de pannes sur des GPU de datacenter | résumés de recherche non relus sur les pages ; aucune source sur les cartes grand public sous charge d'entraînement ; la règle d'amortissement comptable française n'a pas été vérifiée |
| Coût de la mission (Claude Code) | 189 appels, tokens lus dans les journaux de session ; 0,24 à 0,34 Wh par appel ; facteur 10 pour contexte long (hypothèse) | journaux de session les journaux de session de l'outil (mesure exacte des tokens) ; [Google, arXiv 2508.15734](https://arxiv.org/abs/2508.15734) ; [Epoch AI, How much energy does ChatGPT use](https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use) : 0,3 Wh pour une requête GPT-4o typique, hypothèses d'Epoch non relues dans le détail | le nombre de tokens est exact ; l'énergie par appel ne l'est pas : aucune mesure pour Claude, ni pour de très longs contextes |
| Hypothèses sans source | H100 de 700 W, PUE de 1,2, H100 4 à 8 fois plus rapide que la RTX 5070, 11 % d'utilisation du CPU | choix du bilan, modifiables en tête de `bilan_energie.py` | à remplacer par des mesures (HWiNFO ou wattmètre pour le PC, fiche technique du fournisseur pour le cloud) |

## Annexe : coût environnemental de la mission de calcul elle-même (hors projet)

**Cette annexe n'entre dans aucun total du projet** : elle chiffre le travail de calcul environnemental lui-même, mené par Claude Code, en plus des calculs précédents. Il est supposé du même ordre dans un scénario cloud (on ne sait pas comment l'auteur aurait travaillé), donc il ne change pas la comparaison. Les valeurs sont recalculées à chaque génération du rapport, la session n'étant pas terminée. La mission (mesurer, chiffrer et documenter l'énergie, le coût et le CO2 du projet) a été menée par Claude Code dans la session `f5221697` du 24 novembre 2026. Les journaux de session donnent le détail exact : **267 appels au modèle** (Claude Sonnet 5.5 et ses sous-agents de lecture de pages web), 74.1 M de tokens lus dans le cache de contexte, 0.70 M écrits, 0.6 k lus hors cache et **266 k tokens produits**.

| | Valeur | Hypothèse |
|---|---|---|
| Énergie, borne basse | 64 Wh (267 appels x 0.24 Wh) | une requête médiane (Google, mesuré) ; nos appels sont bien plus longs |
| Énergie, borne haute | 0.91 kWh (267 appels x 0.34 Wh x 10) | facteur 10 pour un contexte de 100 000 à 250 000 tokens : **hypothèse sans source**, aucune mesure publiée |
| CO2, réseau américain (384 g/kWh) | 0.025 à 0.35 kg | lieu des serveurs d'Anthropic non précisé |
| CO2, comptabilité « marché » de Google (0,03 g par requête) | 8 g (borne basse seulement) | n'existe pas pour Claude |
| Équivalent en tarif API (jamais payé : forfait) | 11.8 $ HT, soit 12.8 € TTC | 2 $/Mtok hors cache, 0,10 $ lecture de cache, 2,50 $ écriture de cache, 10 $ sortie (Sonnet 5.5, page d'Anthropic lue) |
| Part du total local du bilan | 0.3 à 4 % de l'énergie (20.2 kWh) | |
| Part de l'usage seul (images et texte livrés) | 5 à 68 % de 1334 Wh | |

À titre de comparaison seulement (ces chiffres ne sont dans aucun total du projet) : cette mission représenterait, selon l'hypothèse, de l'ordre de 0.3 % à 4 % de l'énergie de tout le travail local qu'elle chiffre : non négligeable face à l'usage seul (la production des livres), mais faible face à la mise au point. Pour mémoire, l'ensemble des sessions du projet (3 semaines d'orchestration et de scripts) compte 4557 appels et 3.9 M de tokens produits, soit une énergie de 1.1 kWh (borne basse) à 15 kWh (borne haute) : l'orchestration par Claude Code, exclue du bilan comme identique dans les deux scénarios, pèse potentiellement autant que tout le calcul local ; ce chiffre est à citer, avec la même réserve sur l'hypothèse.

Autres éléments de la mission, non chiffrés : les recherches web (énergie des moteurs de recherche, non mesurable), les exécutions de `bilan_energie.py` (quelques secondes de processeur chacune, environ 0,01 kWh au total), le PC allumé pendant la session (déjà allumé sans elle, donc part marginale négligeable) et le trafic réseau de la session.
