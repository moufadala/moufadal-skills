# Definition of Done — Exemples concrets

Ce fichier montre le protocole « vraiment fini » appliqué à différents contextes.
Utilise-le comme inspiration — adapte les catégories au projet réel.

---

## Exemple 1 — PR GitHub / Code

**Contexte** : PR mergée, CI verte. L'utilisateur dit « c'est bon, fini. »

### Suspension
> « Avant de déclarer fini, je mets au clair ce que "vraiment fini" veut dire ici. »

### Inventaire
- ✅ PR mergée dans `main`
- ✅ CI/CD pipeline — vert
- ✅ Tests unitaires — pass
- ✅ Revue approuvée

### Projection
| Point | Statut | Faisable par |
|-------|--------|-------------|
| Protection de branche `main` (PR+CI requis) | ❌ pas activée | utilisateur (permissions GitHub) |
| Release tag + changelog | ❌ pas fait | Hermes |
| Doc mise à jour (README / wiki) | ❌ pas fait | Hermes |
| Rollback documenté (SHA du revert) | ❌ pas fait | Hermes |

### Demande
> « Il reste :
> 1. Protection de branche — nécessite ton action 👉 Settings > Branches > Add rule
> 2. Release tag + changelog — faisable par moi ✅
> 3. Doc README — faisable par moi ✅
> 4. SHA de rollback noté — faisable par moi ✅
>
> Je fais 2-3-4 et tu fais 1 ? Ou c'est bon pour toi comme ça ? »

---

## Exemple 2 — Scraping / Extraction de données

**Contexte** : Script de scraping qui tourne et produit des données.

### Suspension
Idem.

### Inventaire
- ✅ Script scrappe `site-exemple.com` avec curl_cffi
- ✅ Parse les 3 premiers champs OK
- ✅ Export JSON fonctionnel
- ✅ 50 pages testées, pas d'erreur

### Projection
| Point | Statut |
|-------|--------|
| Anti-bot contourné sur TOUS les appels ? | ❌ testé que 50 pages, pas le volume réel |
| Rate limiting / retry implémenté ? | ❌ pas de backoff |
| Rotation user-agent / proxy ? | ❌ IP fixe |
| Dédoublonnage (mêmes données scrapées 2x) ? | ❌ pas de seen tracking |
| Échec partiel : si 5/50 pages échouent, le script crash ou continue ? | ❌ pas de gestion |
| Rapport de fin (combien de succès/échecs) ? | ❌ pas implémenté |

### Demande
> « Le script marche sur 50 pages, mais il manque :
> 1. Rate limiting + retry (backoff exponentiel) — faisable par moi ✅
> 2. Gestion d'échecs partiels (continue sur erreur) — faisable par moi ✅
> 3. Rotation IP (proxy) — nécessite infrastructure (Tailscale ?)
> 4. Rapport de fin avec compteurs — faisable par moi ✅
>
> Je fais 1+2+4. Pour 3, tu veux qu'on utilise le proxy Tailscale ? »

---

## Exemple 3 — Déploiement / Dashboard en ligne

**Contexte** : App immo déployée sur le VPS. L'utilisateur dit « c'est en ligne, fini. »

### Suspension
Idem.

### Inventaire
- ✅ Container Docker tourne
- ✅ Traefik reverse proxy configuré
- ✅ URL `https://immo.148.230.103.174.sslip.io/` accessible
- ✅ Page d'accueil s'affiche

### Projection
| Point | Statut |
|-------|--------|
| HTTPS / certificat valide ? | ✅ déjà OK |
| Pages internes (recherche, login, API) fonctionnelles ? | ❌ testé que page d'accueil |
| Responsive mobile ? | ❌ pas vérifié |
| Erreurs console JS / 404 assets ? | ❌ pas vérifié (ouvrir DevTools) |
| Limites de ressources (RAM, CPU) ? | ❌ pas monitoré |
| Backup / rollback du déploiement ? | ❌ pas de procédure |
| CNAME / DNS propre (pas IP nue) ? | ❌ sous-domaine sslip.io uniquement |

### Demande
> « L'app est en ligne, mais avant de dire fini :
> 1. Smoke test des routes principales (recherche, API) — faisable par moi ✅
> 2. Vérification responsive mobile — faisable (ouvrir DevTools) ✅
> 3. Erreurs console JS — faisable ✅
> 4. CNAME propre (ex: immo.monsite.com) — nécessite DNS chez Hostinger
> 5. Script de rollback — faisable par moi ✅
>
> Je fais 1+2+3+5. Pour le 4, tu as accès au DNS Hostinger ? »

---

## Exemple 4 — Recherche / Analyse

**Contexte** : Hermes a fait une recherche sur les modèles LLM et rédigé 3 pages de synthèse.

### Suspension
Idem.

### Inventaire
- ✅ Recherche web sur 5 sources
- ✅ Synthèse rédigée avec sections
- ✅ Tableau comparatif des modèles
- ✅ Liens sources en bas de page

### Projection
| Point | Statut |
|-------|--------|
| Sources vérifiées (liens cliquables, pas morts) ? | ❌ pas cliqué |
| Date de la recherche (les modèles bougent vite) ? | ❌ pas de timestamp |
| Contradictions entre sources détectées ? | ❌ pas vérifié |
| « Je ne sais pas » marqué sur ce qui n'est pas trouvé ? | ❌ pas de limites explicites |
| Format livrable (Markdown, PDF, message clair) ? | ⚠️ dépend de l'usage |

### Demande
> « La synthèse est prête, mais :
> 1. Vérification des liens (click test rapide) — faisable par moi ✅
> 2. Ajout date + clause de fraîcheur — faisable ✅
> 3. Marquer les trous / incertitudes — à voir si pertinent
> 4. Export PDF si besoin — faisable ✅
>
> Je fais 1+2+4. Tu veux autre chose ? »

---

## Exemple 5 — Installation / Config VPS

**Contexte** : Mise en place d'un nouveau service (ex: Firecrawl, SearXNG).

### Suspension
Idem.

### Inventaire
- ✅ Package installé
- ✅ Config de base écrite
- ✅ Service/systemd démarre
- ✅ Port UFW ouvert
- ✅ Test curl local OK

### Projection
| Point | Statut |
|-------|--------|
| Démarrage au boot (systemd enable) ? | ❌ pas fait |
| Logs vérifiés (pas d'erreur silencieuse) ? | ❌ `journalctl` non consulté |
| Limites de ressources (RAM max, OOM) ? | ❌ pas configuré |
| Mise à jour / maintenance (cron de mise à jour ?) | ❌ pas prévu |
| Intégration avec les services existants (Traefik, Hermes) ? | ❌ pas testé |
| Rollback (commande de désinstallation propre) ? | ❌ pas documenté |

### Demande
> « Le service fonctionne manuellement, mais :
> 1. Enable au boot — faisable ✅
> 2. Vérification des logs pour erreurs cachées — faisable ✅
> 3. Limite mémoire Docker (512M ?) — faisable ✅
> 4. Intégration Traefik (sous-domaine) — faisable ✅
> 5. Commande de rollback documentée — faisable ✅
>
> Je fais tout ça, ou tu préfères d'abord valider le fonctionnement de base ? »
