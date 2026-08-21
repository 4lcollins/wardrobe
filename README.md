# Wardrobe

Wardrobe is a personal clothing management app that helps you organize, track, and plan your outfits. Easily catalog your Wardrobe, create outfit combinations, and get suggestions based on your preferences and the weather.

## Shiny app

Run the Shiny app locally from the project root:

```sh
make run
```

Shiny application code lives in `web/`, while backend logic and services live in `src/`.

## Deployment

Before deploying to Posit Connect Cloud, sync the locked dependencies into `requirements.txt`:

```sh
make requirements
```

Use the Posit Publisher VS Code extension to create or update the Shiny deployment.

## Automations

Daily briefs run from GitHub Actions in `.github/workflows/daily-brief.yml`.

Required configuration:

- `GEMINI_API_KEY`
- `GMAIL_APP_PASSWORD`
- `OPENWEATHERMAP_KEY`
- `SENDER_EMAIL`
- `SUPABASE_KEY`
- `SUPABASE_URL`

## Supabase

The initial schema lives in `supabase/migrations/`. The app uses active rows in the Supabase `users` table for email automation recipients.
