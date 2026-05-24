# Auto-deploy via GitHub Actions

## What changed

Render's GitHub App webhook was not firing on pushes to `master`, so the Render
service stopped picking up new commits automatically. Rather than fighting the
Render dashboard / GitHub App permissions, we sidestep the problem entirely:
GitHub Actions now calls Render's deploy API directly on every push.

This **replaces** the need to repair Render's webhook via the dashboard. You
don't have to reconnect the GitHub App, re-grant permissions, or do anything
in the Render UI.

## The new flow

1. You `git push` to `master` (or merge a PR into `master`).
2. GitHub Actions runs `.github/workflows/deploy.yml`.
3. The workflow POSTs to
   `https://api.render.com/v1/services/<service-id>/deploys` with the
   `RENDER_API_KEY`.
4. Render queues a fresh deploy of the current commit.
5. The workflow polls the deploy status for up to ~10 minutes and marks the
   run green when status becomes `live`, red if Render reports
   `build_failed` / `update_failed` / `canceled` / `deactivated` /
   `pre_deploy_failed`.
6. The README badge at the top of the repo reflects the most recent run.

## Concurrency

The workflow uses a `render-deploy` concurrency group with
`cancel-in-progress: true`. If you push twice in quick succession, the older
run is cancelled and only the latest commit is deployed. No stacked deploys,
latest wins.

## Secrets

Stored on the repo (not in code):

- `RENDER_API_KEY` — Render personal API token used to call the deploy API.
- `RENDER_SERVICE_ID` — the `srv-...` id of the playship-landing service.

The key only appears in the workflow as `${{ secrets.RENDER_API_KEY }}` and
is masked in Actions logs by GitHub. Never paste it into commit messages,
issues, or chat.

## What you need to do

**Nothing.** Just keep pushing to `master`. Deploys are automatic.

If a deploy fails, the workflow run on
[github.com/avisre/playship-landing/actions](https://github.com/avisre/playship-landing/actions)
will be red — open it and read the `Trigger Render deploy` or
`Poll deploy status` step logs to see what Render said.

## Rotating the API key

1. Generate a new key in Render dashboard -> Account Settings -> API Keys.
2. `gh secret set RENDER_API_KEY --body "<new key>" --repo avisre/playship-landing`
3. Revoke the old key in Render.

No code changes required.

## Why this is better than the GitHub App webhook

- Visible: every deploy attempt has a GitHub Actions run with logs.
- Debuggable: failures surface as red checks on GitHub, not silent skips.
- Portable: switching hosting providers means swapping the curl call, not
  re-wiring webhooks.
- Doesn't depend on Render's GitHub App being healthy.
