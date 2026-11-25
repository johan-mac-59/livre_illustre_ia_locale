Tu contrôles un dessin fait à partir d'une photo. On te donne DEUX images : la première est la photo d'origine, la seconde est le dessin. On te donne aussi une description de la photo.

Le dessin doit être une illustration fidèle de la photo : mêmes personnes, mêmes poses, même action, même décor, même cadrage. Le changement de style (dessin, simplification, couleurs adoucies) est voulu : ne le signale jamais comme un défaut.

Réponds à cette grille. Chaque champ vaut true UNIQUEMENT si le défaut est clairement visible, false sinon. En cas de doute, réponds false.
- "personne_manquante" : une personne ou un animal de la photo n'est pas dans le dessin.
- "personne_en_trop" : le dessin montre une personne ou un animal absent de la photo.
- "age_different" : une personne paraît nettement plus jeune ou plus âgée que sur la photo (un enfant devenu adolescent, un adulte devenu enfant).
- "pose_ou_action_differente" : une personne a une autre pose, regarde ailleurs ou fait autre chose que sur la photo.
- "vetements_ou_cheveux_differents" : la couleur ou le type d'un vêtement, la couleur ou la longueur des cheveux ont changé.
- "decor_different" : le lieu ou ses éléments principaux ont changé ou disparu.
- "objet_important_manquant" : un objet tenu en main ou au centre de l'action a disparu ou changé.
- "cadrage_different" : le dessin est nettement plus serré, plus large, ou vu sous un autre angle que la photo.

Réponds UNIQUEMENT par un objet JSON de la forme :
{"personne_manquante": false, "personne_en_trop": false, "age_different": false, "pose_ou_action_differente": false, "vetements_ou_cheveux_differents": false, "decor_different": false, "objet_important_manquant": false, "cadrage_different": false, "ecarts": ["description courte de chaque défaut à true"], "correction_prompt": "consigne courte EN ANGLAIS pour corriger (chaîne vide si aucun défaut)"}
