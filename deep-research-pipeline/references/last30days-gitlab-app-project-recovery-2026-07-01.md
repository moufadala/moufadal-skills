# Last30days recovery for GitLab-hosted app projects

## Context

When Moufadal asks for “Last30days” on an app/project and specifically wants recent news plus “issues ouvertes / MR ouvertes”, Last30days may underperform if the project is primarily hosted on GitLab. In one F-Droid client check, Last30days returned mostly Reddit/HN tangential mentions and only a GitHub ecosystem item, while the authoritative activity was on GitLab `fdroid/fdroidclient`.

## Reusable pattern

1. Run Last30days first for public/social/community signal and coverage diagnostics.
2. Identify the authoritative forge from the project’s real homepage/repo. Do not assume GitHub.
3. If the repo is GitLab, supplement with GitLab API calls:

```bash
PROJECT='namespace%2Fproject'
BASE="https://gitlab.com/api/v4/projects/$PROJECT"

curl -sS -L "$BASE/releases?per_page=20"
curl -sS -L "$BASE/repository/tags?per_page=20"
curl -sS -L "$BASE/issues?created_after=YYYY-MM-DDT00:00:00Z&order_by=created_at&sort=desc&per_page=30"
curl -sS -L "$BASE/issues?state=opened&updated_after=YYYY-MM-DDT00:00:00Z&order_by=updated_at&sort=desc&per_page=30"
curl -sS -L "$BASE/merge_requests?state=opened&updated_after=YYYY-MM-DDT00:00:00Z&order_by=updated_at&sort=desc&per_page=30"
curl -sS -L "$BASE/merge_requests?state=merged&updated_after=YYYY-MM-DDT00:00:00Z&order_by=updated_at&sort=desc&per_page=30"
```

4. Parse counts, top titles, labels, dates, and web URLs. Group findings into:
   - releases/tags;
   - open issues recently updated;
   - new issues created in window;
   - open MRs;
   - recently merged MRs;
   - community/social chatter from Last30days.
5. Separate “public/news signal” from “development activity signal”. Low press/social volume does not mean low project activity.
6. When Last30days reports missing X/Twitter or thin web coverage, mention it as a coverage limitation, not as a failure of the whole research if authoritative forge evidence is strong.

## F-Droid-specific notes from 2026-07-01 run

- Authoritative client repo: `https://gitlab.com/fdroid/fdroidclient`.
- Recent activity centered on `2.0-alpha10` and preparation of 2.0 stable.
- Useful GitLab labels to surface: `help-wanted`, `ui`, `regression`, `security`, `swap`, `ci`, `localization`.
- Last30days public/social results were thin and tangential; GitLab API was the reliable source for issues/MRs.

## Pitfall

Do not pass `--github-repo` for a GitLab-hosted project and treat the sparse GitHub result as authoritative. Use forge-specific APIs after Last30days if the task asks for open issues/MRs or current development status.
