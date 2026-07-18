# News/watch dashboard product contract — session-derived reference

Use when building a news, local-events, classified-announcement, monitoring, or briefing dashboard where the user has not manually specified every UX rule. This is a reusable product default, not a one-off implementation note.

## Core verdict

A watch/news dashboard is a **decision tool**, not a card gallery. Each item should answer:

1. Why should I look at this?
2. Is it urgent or recent?
3. Is it trustworthy?
4. Is it relevant to me?
5. What action can I take now?

Build around the workflow:

```text
Discover → Understand → Decide → Act → Stop seeing noise
```

not:

```text
Render many cards + generic filters
```

## Research anchors

- NN/g Cards: cards summarize a conceptual unit, provide information scent, and often link to detail. They may include title, summary, timestamp, metadata, sharing/secondary CTA.
- NN/g Filters: filter design depends on user intent. Exploratory users benefit from interactive filters; specific-goal users need stable filtering that does not disrupt context.
- Dashboard UX patterns: dashboards should expose actionable insights and system status; showing all data is worse than showing the right data.
- Useful dashboard principle: a dashboard should be glanceable and decision-oriented; in 5 seconds the user should know what matters and what to do next.
- Feed readers / monitoring tools such as Inoreader emphasize filtering noise, saving items, tags/rules, read-later, and automation.

## Default acceptance contract

A news/watch dashboard is acceptable only if:

### First screen

- Shows `À traiter maintenant` or equivalent, not just stats.
- Displays 3–5 top priorities before heavy scrolling, especially on mobile.
- Shows last update and source health/freshness.

### Card fields

Each card should include, when available:

- title;
- type/category: news, event, real-estate, training, etc.;
- source label and trust status;
- publication date;
- event/deadline date if relevant;
- location/zone if relevant;
- short summary;
- explicit priority reason (`Pourquoi c’est prioritaire`);
- badges: new, urgent, source reliable, to verify, seen/saved/hidden.

### Priority model

Priority should be explainable. Suggested factors:

```text
+ freshness / publication recency
+ deadline or event soon
+ source reliability / probed status
+ personal/project-relevant theme
+ location relevance
+ new/unseen state
+ completeness: date, location, source URL, summary
- duplicate probable
- weak/broken/unverified source
- stale or non-actionable item
```

Expose the human reason, not only a numeric score.

### Click and action model

- Card click: select item and open detail inside the dashboard.
- External URL: separate `Ouvrir source ↗` button; open in new tab/window.
- Never make the entire card an external link when it also has secondary actions.
- Mobile targets must be large and visually distinct.
- Important actions: `Vu`, `Garder`, `Masquer`, `Ouvrir source`; optional next step: `Copier dans brief` / share.
- Persist user state at least in localStorage for a prototype; use durable project state for production.

### Filters/search

Prefer decision-oriented filters:

- À traiter;
- Aujourd’hui / 7 jours;
- Non lus;
- Gardés;
- À vérifier;
- Sources fiables;
- Sorties / Actus / category;
- Source, location, theme, date range where useful.

Filters should have counts when practical and should not unexpectedly destroy the current selection.

Search should cover title, summary, source, location, category, date, tags, and priority reason.

### Empty/error/stale states

Handle:

- no results;
- source unavailable or blocked;
- item without location/date;
- invalid source link;
- stale data;
- probable duplicate;
- unverified source/item.

## QA gates beyond technical DOM checks

For this class of UI, QA must prove product value:

- raw first-paint HTML is non-empty before JavaScript enhancement;
- top priorities are visible and meaningful in a 5-second scan;
- at least one item has a visible priority reason;
- card click does not navigate away and updates detail;
- `Ouvrir source ↗` opens the correct external URL for representative items;
- save/seen/hide state changes visibly and persists after reload;
- filters/search return expected counts and maintain UI stability;
- mobile viewport around 390px is usable;
- console has no blocking errors;
- source/data freshness and failure states are visible.

## Implementation implications

When upgrading an existing generic feed dashboard, add to the item model:

```text
priority_level
priority_reason
trust_status
user_state: seen/saved/hidden/copied
source_health
is_duplicate_candidate
```

Then rebuild cards and tests around these semantics before improving visual polish.
