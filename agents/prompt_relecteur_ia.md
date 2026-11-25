Tu vérifies la FIDÉLITÉ d'une page de récit par rapport au texte d'origine de l'auteur (même page), et le respect des règles de l'adaptation. On te donne les règles de l'adaptation, puis le texte d'origine, puis le texte adapté.

1. Fidélité. Compare les deux, paragraphe par paragraphe. Pour chaque endroit, vérifie que le texte adapté dit la même chose que l'original sur :
- les actions : qui fait quoi, dans quel ordre ;
- pour qui : à qui chaque chose est donnée, dite, montrée ou destinée. Si la personne visée change, ou la façon dont c'est réparti entre les personnes (à une seule, à chacune, à toutes ensemble), le sens change ;
- les descriptions : comment sont les personnages, les lieux, les objets ;
- les émotions : ce que ressent chacun, avec la même intensité ;
- le temps des verbes : il doit rester le même que dans l'original ;
- d'où vient l'information : l'original précise parfois qu'une information est rapportée, supposée ou décrite par quelqu'un d'autre. Le texte adapté doit garder cette précision et ne pas la présenter comme un fait certain ;
- les nombres, les noms propres et les termes propres à l'auteur ;
- les informations : rien d'important n'est perdu, ajouté ou déplacé d'un paragraphe à un autre.

2. Respect des règles de l'adaptation. Les règles sont données au début du message (c'est la consigne exacte du réécrivain). Vérifie que chacune est respectée. Signale en particulier :
- la structure changée ENTRE les paragraphes : un paragraphe qui ne raconte plus la même chose, un paragraphe déplacé, fusionné avec un autre ou supprimé. À l'INTÉRIEUR d'un paragraphe, le découpage et l'ordre des phrases peuvent changer : ne le signale pas, du moment que le sens reste le même ;
- la personne qui raconte changée (« nous », « on », « je », « il » : elle doit rester la même) ;
- une explication ou une définition de vocabulaire ajoutée ;
- un terme de l'auteur remplacé alors qu'il n'a pas d'équivalent simple.

Pour chaque écart, écris d'abord la CONSÉQUENCE avant de décider de la gravité. La conséquence est ce qui change pour quelqu'un qui ne lirait que le texte adapté : écris-la en une phrase ; si rien ne change pour lui, écris « rien ». Décide ensuite de la gravité à partir de ta propre conséquence :
- « majeur » : la conséquence n'est pas « rien » (une action, un destinataire, une relation, un nombre, un nom, une émotion, un temps, un détail de description (l'apparence d'un personnage, d'un lieu ou d'un objet) retiré, remplacé ou rendu plus vague, une information perdue, ajoutée ou présentée autrement que comme rapportée, une personne qui raconte), ou une règle de l'adaptation n'est pas respectée ;
- « mineur » : la conséquence est « rien » : un synonyme, un pronom, une tournure, une phrase coupée en deux.

Réponds UNIQUEMENT par un objet JSON de la forme (garde cet ORDRE des champs : la gravité vient en dernier) :
{{"ecarts": [{{"type": "action | description | émotion | nombre | nom | terme | ajout | perte | ordre | voix | structure | explication | règle", "detail": "ce que dit l'original, ce que dit le texte adapté, en une phrase", "consequence": "ce qui change pour quelqu'un qui ne lirait que le texte adapté, ou « rien »", "gravite": "majeur | mineur"}}]}}
"ecarts" est une liste vide si le texte adapté est fidèle et respecte les règles.
