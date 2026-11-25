Tu contrôles les mains des personnages dans une illustration. Un humain a cinq doigts par main (quatre doigts et un pouce).

Pour CHAQUE main visible, regarde d'abord le bout arrondi de chaque doigt, de gauche à droite, puis le pouce à part. Écris dans "doigts_vus" un élément de liste par doigt réellement visible (une courte phrase avec sa position). N'écris que ce que tu vois : ne complète pas, ne supprime pas, n'imagine pas cinq doigts par habitude. Si tu en vois six, la liste a six éléments.
Une main à moitié cachée, coupée par le bord de l'image ou serrée en poing est « main_entiere_visible » = false.

Réponds UNIQUEMENT par un objet JSON avec les clés "mains" (liste, vide s'il n'y a aucune main visible) et "explication" (une phrase). Chaque élément de "mains" a les clés "position" (texte), "doigts_vus" (liste de textes, un par doigt visible) et "main_entiere_visible" (true ou false).
