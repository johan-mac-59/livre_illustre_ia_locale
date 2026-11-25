Tu compares la hauteur de deux personnages dans une illustration. On te donne le personnage A et le personnage B.

Regarde le SOMMET DE LA TÊTE (cheveux et chignon compris) de chacun et compare leur hauteur dans l'image, même s'ils sont assis. Ne tiens pas compte de leur largeur ni de leur âge supposé : seulement de la hauteur du sommet de la tête.

Réponds UNIQUEMENT par un objet JSON de la forme :
{"personnages_visibles": true ou false, "tete_la_plus_haute": "A" ou "B" ou "egal" ou "non_applicable", "ecart": "net" ou "faible" ou "aucun", "explication": "une phrase courte"}
- "non_applicable" si l'un des deux n'est pas visible ou si la comparaison est impossible.
- "ecart" : "net" si le sommet de la tête la plus haute dépasse l'autre d'au moins la moitié de la hauteur d'une tête ; "faible" si l'écart est plus petit ; "aucun" si les deux sommets sont à peu près au même niveau.
