# Wardrobe

Wardrobe is a personal clothing management app that helps you organize, track, and plan your outfits. Easily catalog your Wardrobe, create outfit combinations, and get suggestions based on your preferences and the weather.

## Shiny app

Run the Shiny app locally from the project root:

```sh
make run
```

Shiny application code lives in `shiny_app/`, while backend logic and services live in `src/`.

## Deployment

Before deploying to Posit Connect Cloud, sync the locked dependencies into `requirements.txt`:

```sh
make requirements
```

Use the Posit Publisher VS Code extension to create or update the Shiny deployment.

## Automations

Daily briefs run from GitHub Actions in `.github/workflows/daily-brief.yml`. The workflow can be queued manually from GitHub or by its schedule.

Configure these repository secrets before running it:

- `GEMINI_API_KEY`
- `GMAIL_APP_PASSWORD`
- `OPENWEATHERMAP_KEY`
- `RECIPIENT_EMAILS`
- `SENDER_EMAIL`

Put recipient addresses in `RECIPIENT_EMAILS` as a comma- or newline-separated list. Keep it as a secret so the list is editable in GitHub but not visible in the repo or workflow logs.
