# Brief/dashboard de veille — style clair type MIAM

Session signal: l'utilisateur a rejeté un dashboard noir/générique jugé « moche » et trop dev/SaaS. Pour les veilles locales, morning briefs, dashboards éditoriaux ou outils de lecture rapide, privilégier une interface claire, chaleureuse, priorisée et orientée décision.

## Direction visuelle

- Pas de dark dashboard générique sauf demande explicite.
- Fond clair/crème, surfaces blanches ou ivoire, contraste doux mais lisible.
- Typographie éditoriale/humaine; Montserrat fonctionne bien si la référence MIAM est demandée.
- Rythme visuel chaleureux: grands titres, sous-titres utiles, cartes aérées, micro-copies courtes.
- Éviter le vocabulaire SaaS froid: métriques arbitraires, grids uniformes, glow/gradients, cartes noires.

## Structure d'information recommandée

1. **Résumé 1 minute en premier**
   - Ce qu'il faut retenir maintenant.
   - Pourquoi c'est utile.
   - Éventuellement 3 priorités max.
2. **Flux priorisé**
   - Important / À lire / Sorties / Opportunités / À surveiller.
   - Ne pas afficher un mur de doublons; dédupliquer avant rendu.
3. **Progressive disclosure**
   - Titre + source + raison d'intérêt visibles.
   - Détail/résumé long au clic via accordéon.
4. **Actions concrètes**
   - À faire bientôt.
   - À surveiller.
   - Sources testées ou état de couverture.
5. **Filtres simples**
   - Tout / Important / Actus / Sorties ou catégories métier.
   - Recherche par mot-clé si le flux dépasse quelques dizaines d'items.

## Vérification attendue

- Ouvrir le fichier en navigateur si possible.
- Tester au moins un accordéon/détail au clic.
- Tester les filtres ET la recherche quand ces contrôles sont présents.
- Tester explicitement le clic sur une carte de sortie/actu : le détail doit s’ouvrir sans erreur et le lien source doit rester accessible.
- Pour une version “livrable maintenant”, préférer un item sélectionnable + panneau lecteur + bouton source séparé, afin d’éviter les cartes-liens ambiguës qui cassent le détail au clic.
- Vérifier les comptes après filtres (ex. sorties seulement, actus seulement, sources robustes seulement) plutôt que seulement l’existence des boutons.
- Vérifier console JS = 0 erreur quand les outils navigateur sont disponibles.
- Mentionner explicitement ce qui a été vérifié dans la réponse finale.

## Anti-patterns observés

- Dashboard sombre plein de cartes et de chiffres: mauvais fit pour un brief de veille locale.
- Tout afficher au même niveau: fatigue de lecture.
- Résumés longs directement visibles: empêche le scan rapide.
- Dire que c'est inspiré d'une référence sans avoir réellement inspecté son vocabulaire visuel.