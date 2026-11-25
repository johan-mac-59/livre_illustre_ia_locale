Tu contrôles le style d'une image qui doit être une illustration de livre pour enfants. On te donne UNE image et le style demandé.

Réponds à cette grille. Chaque champ vaut true UNIQUEMENT si le défaut est clairement visible, false sinon. En cas de doute, réponds false.
- "rendu_photographique" : l'image ressemble encore à une photo, ou à une photo passée dans un filtre (textures réelles, éclairage photographique, visages photographiques), plutôt qu'à un dessin fait à la main.
- "style_non_conforme" : la technique visible est nettement différente du style demandé (par exemple rendu 3D, manga, peinture à l'huile réaliste alors qu'on demande de la gouache).
- "visage_deforme" : un visage est déformé, flou, fondu ou a des traits en trop ou manquants.
- "inquietant" : l'image est effrayante ou dérangeante pour un enfant.

Réponds UNIQUEMENT par un objet JSON de la forme :
{"rendu_photographique": false, "style_non_conforme": false, "visage_deforme": false, "inquietant": false, "ecarts": ["description courte de chaque défaut à true"], "correction_prompt": "consigne courte EN ANGLAIS pour corriger (chaîne vide si aucun défaut)"}
