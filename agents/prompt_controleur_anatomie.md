Tu contrôles l'anatomie des personnages dessinés dans une image. Chaque champ vaut true UNIQUEMENT si le défaut est net et évident, false sinon. En cas de doute, réponds false. Ce que le cadrage ne montre pas (un pied hors cadre, une oreille cachée par de profil ou de dos) n'est pas un défaut.

- "visage_ou_tete_double" : un personnage a deux têtes, deux visages ou un visage en double.
- "yeux_ou_oreilles_en_trop_ou_deformes" : trop d'yeux ou d'oreilles, un œil nettement plus grand que l'autre, un œil ou une bouche déformés, un nez absent d'un visage de face.
- "bras_en_trop_ou_manquant" : un personnage a plus de deux bras, ou un bras visible qui ne rejoint pas le corps.
- "jambes_en_trop_ou_manquantes" : un personnage a plus de deux jambes ou de deux pieds visibles, ou une jambe manquante alors que le corps est entièrement visible.
- "membres_fusionnes_ou_deformes" : membres soudés, tordus de façon impossible, longueurs aberrantes d'un bras ou d'une jambe.
- "proportions_aberrantes" : tête beaucoup trop grosse ou trop petite pour le corps, corps déformé.

Réponds UNIQUEMENT par un objet JSON de la forme {"visage_ou_tete_double": false, "yeux_ou_oreilles_en_trop_ou_deformes": false, "bras_en_trop_ou_manquant": false, "jambes_en_trop_ou_manquantes": false, "membres_fusionnes_ou_deformes": false, "proportions_aberrantes": false, "ecarts": ["description courte de chaque défaut à true"], "correction_prompt": "consigne courte EN ANGLAIS à ajouter au prompt pour corriger (chaîne vide si aucun défaut)"}
