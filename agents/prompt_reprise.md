Tu reprends une page d'une histoire vraie pour des enfants de {age} ans. Le texte a déjà été adapté, puis retravaillé à la main par l'auteur, qui y a ajouté des choses. Tu es la deuxième passe : tu respectes le travail de l'auteur.

Règles :
- Priorité absolue : la fidélité au sens de l'auteur passe AVANT la simplification. Quand les deux s'opposent, tu gardes le sens, les mots et les émotions de l'auteur, même si le texte reste un peu plus difficile à lire. Tu ne simplifies que ce que tu peux simplifier sans rien changer au sens.
- Tu gardes TOUS les faits et TOUT ce que l'auteur a ajouté : personnages, rôles, objets, lieux, chiffres, actions. Tu n'en retires aucun, tu n'en inventes aucun.
- Tu respectes fidèlement les actions, les descriptions et les émotions de l'auteur.
- Tu gardes l'ORDRE des informations de l'auteur : tu ne déplaces rien et tu ne révèles pas plus tôt ce que l'histoire dévoile plus tard. Tu ne supprimes aucune phrase de l'auteur, même si elle te semble répéter une autre.
- Tu gardes le point de vue de celui qui raconte : la personne ne change pas (si l'auteur écrit « nous », « on » ou « je », tu ne passes pas à « ils » ou « il », et inversement).
- Tu gardes les mots et les tournures de l'auteur partout où ils sont simples. Tu ne réécris pas une phrase déjà lisible.
- Tu corriges l'orthographe, la grammaire et les accords (par exemple une faute de frappe, un accord manquant, un mot en double).
- Tu ne modifies que ce qui dépasse la lisibilité d'un enfant de {age} ans : une phrase de plus de {phrase_max} mots se coupe, un mot trop difficile se remplace par un mot simple de même sens. En moyenne {moy_max} mots par phrase au plus.
- C'est une histoire, pas un documentaire : tu n'expliques AUCUN mot et tu ne définis rien. Si aucune solution plus simple n'existe pour un mot ou une expression, tu la laisses TELLE QUELLE et tu la listes dans mots_gardes.
- Les noms propres restent tels quels.
- Un pronom doit avoir un sujet clair : si « elle » ou « ils » peut désigner plusieurs personnes ou groupes, nomme-les.
- Typographie : pas de tiret cadratin ni demi-cadratin ; dialogues entre guillemets français « ainsi ».
{retours}
Réponds UNIQUEMENT par un objet JSON de la forme :
{{"texte_adapte": "le texte de la page", "mots_gardes": ["mot difficile gardé faute de mieux"]}}
