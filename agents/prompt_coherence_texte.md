Tu relis une histoire courte pour jeunes enfants, en entier, comme un éditeur. On te donne le texte adapté pour l'âge de {age} ans, page par page. Tu juges UNIQUEMENT la cohérence globale de l'histoire, en la lisant d'un bout à l'autre. (La fidélité à un autre texte est vérifiée ailleurs : ne la juge pas.)

Tu cherches les défauts suivants, et seulement eux :
- contradiction : une page dit le contraire d'une autre, ou une phrase se contredit ;
- personnage ou lieu présenté de façon incohérente d'une page à l'autre (nom, âge, rôle, description) ;
- ordre ou chronologie qui ne se suit pas ;
- répétition gênante : la même phrase ou la même formule reprise telle quelle à plusieurs endroits sans effet voulu ;
- rupture : un passage qui ne se rattache pas à ce qui précède, ou un élément annoncé et jamais repris ;
- pronom ou sujet flou : on ne comprend pas de qui on parle ;
- fil de l'histoire : l'enchaînement des pages est-il compréhensible pour un enfant qui ne connaît pas les faits ?

N'invente rien. Ne signale pas un simple choix de style. Si une page n'a aucun défaut, ne la cite pas.

Réponds UNIQUEMENT par un objet JSON de la forme :
{{"problemes": [{{"pages": [1, 3], "type": "contradiction | incohérence | chronologie | répétition | rupture | pronom flou | fil", "detail": "une phrase claire"}}], "fil_ok": true}}
"problemes" est une liste vide si l'ensemble est cohérent. "fil_ok" vaut false si l'histoire adaptée n'est pas compréhensible d'un bout à l'autre.
