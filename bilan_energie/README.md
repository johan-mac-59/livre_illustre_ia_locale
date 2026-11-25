# Local ou cloud : énergie, coût et CO2 d'un projet d'IA générative sur des données personnelles

Comparatif mesuré (et non estimé quand c'était possible) du travail fait **en local** sur une machine à 1357 € et du même travail refait **dans le cloud** : entraînement de 4 modèles de visages (LoRA), 1358 images générées, 5132 appels de modèles de texte, deux livres illustrés de trois histoires chacun. Généré le 2026-11-25.

| | Local | Cloud |
|---|---|---|
| Coût TTC | **35 €** (électricité 4,05 € + amortissement 30 € en comptant la garantie constructeur de chaque composant, 11 € avec des durées de vie plus ambitieuses) | **81 €** en API, **53 à 97 €** en GPU loué |
| Énergie | 20,2 kWh | 9,7 à 18,8 kWh |
| CO2 | 1,05 kg (réseau français) | 3,7 à 7,2 kg (réseau américain supposé) |

Ces chiffres sont des **minimums** reposant sur des hypothèses explicites pour le cloud ; l'entraînement des modèles eux-mêmes et la fabrication du matériel ne sont pas comptés (non calculables). Les limites, les sources et la souveraineté des données sont détaillées dans le rapport.

## Contenu

- [bilan_energie.pdf](bilan_energie.pdf) : rapport complet (méthode, résultats, limites, sources), version [Markdown](bilan_energie.md)
- [carrousel_linkedin.pdf](carrousel_linkedin.pdf) : synthèse en 7 diapositives
- [donnees_calcul.json](donnees_calcul.json) : données agrégées et paramètres qui ont servi au calcul
- [METHODE.md](METHODE.md) : comment refaire, poursuivre et dupliquer le bilan

Aucune donnée personnelle : les personnes sont désignées « personnage 1 à 4 » et les histoires « histoire 1 à 3 ».
