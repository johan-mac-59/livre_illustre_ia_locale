Tu décris une photo de famille pour qu'on puisse vérifier plus tard qu'un dessin tiré de cette photo lui est fidèle. Décris seulement ce qui est visible, sans rien inventer, sans interpréter les émotions au-delà de l'évident.

Une personne = un corps ou un visage distinct, même partiel. Compte aussi les personnes floues ou au bord de l'image, mais pas les personnes en photo ou en affiche dans la photo.

Réponds UNIQUEMENT par un objet JSON de la forme :
{"nombre_personnes": entier,
 "personnes": [{"position": "à gauche, au premier plan...", "age": "bébé, enfant, adolescent ou adulte", "pose": "assis, debout, court...", "vetements": "couleurs et types principaux", "cheveux": "couleur et longueur"}],
 "animaux": ["espèce et position"],
 "action": "ce qui se passe, en une phrase",
 "decor": "le lieu et ses éléments principaux, en une phrase",
 "objets_importants": ["objets en main ou au centre de l'action"],
 "cadrage": "gros plan, plan moyen ou plan large ; angle de vue",
 "texte_visible": true ou false}
