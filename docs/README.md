# Documentation

## Architecture d'un agent

Cette proposition décrit une architecture pragmatique pour un agent capable de suivre des instructions, d'utiliser des skills basés sur MCP, de maintenir une mémoire utile et d'orchestrer un réseau d'agents spécialisés.

### 1) Couche d'instructions

- **Instructions système**: contraintes globales, sécurité, style de réponse.
- **Instructions développeur**: conventions de projet, standards techniques.
- **Instructions utilisateur**: intention métier et objectifs de la tâche.
- **Priorité**: système > développeur > utilisateur > contexte mémoire.

L'agent construit un plan d'exécution à partir de ces couches avant d'appeler des outils.

### 2) Couche de skills (capacités MCP)

Un **skill** encapsule un workflow réutilisable:

- découverte d'une capacité via MCP,
- validation des entrées,
- exécution d'outils,
- restitution structurée du résultat.

L'agent sélectionne le skill le plus pertinent selon:

1. l'intention détectée,
2. les contraintes de coût/latence,
3. le niveau de confiance attendu.

### 3) Couche mémoire

La mémoire combine plusieurs niveaux pour rester performante et explicable:

- **Mémoire conversationnelle courte**: fenêtre de contexte active.
- **Index sémantique à la volée**: embeddings en mémoire (ou stockage léger fichier) pour retrouver les passages pertinents.
- **Store clé/valeur**: concepts, décisions, préférences utilisateur, thèmes récurrents.
- **Index graphe** *(optionnel)*: relations entre entités, idées, tâches et dépendances.

#### Politique de lecture/écriture

- Écriture après chaque étape significative (résultat d'outil, décision, validation).
- Lecture sélective avant planification et avant réponse finale.
- Nettoyage périodique: fusion des doublons, expiration des données obsolètes.

### 4) Réseau d'agents

L'architecture peut déléguer à des agents spécialisés:

- **Agent orchestrateur**: reçoit l'objectif global et découpe en sous-tâches.
- **Agents experts**: exécutent des tâches ciblées (recherche, code, analyse, QA).
- **Agent synthèse**: consolide les sorties et produit une réponse finale cohérente.

#### Boucle de délégation

1. Planifier et découper.
2. Déléguer avec contrat d'interface clair (input/output).
3. Vérifier qualité et cohérence.
4. Reprendre la main pour arbitrer et répondre.

### 5) Flux d'exécution (résumé)

1. Comprendre la demande + contraintes.
2. Charger instructions et mémoire utile.
3. Sélectionner skill(s) MCP.
4. Exécuter outils / déléguer à des sous-agents.
5. Évaluer les résultats (fiabilité, complétude, sécurité).
6. Mettre à jour la mémoire.
7. Produire la réponse finale.

### 6) Observabilité minimale recommandée

- logs structurés par étape,
- traces d'appels outils/skills,
- métriques de latence/coût/taux d'échec,
- score de confiance par réponse.

Cette base peut ensuite être enrichie avec des garde-fous de sécurité, des politiques de confidentialité et des évaluations automatiques de qualité.
