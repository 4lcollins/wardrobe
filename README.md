# Wardrobe

Wardrobe is a personal clothing management app that helps you organize, track, and plan your outfits. Easily catalog your Wardrobe, create outfit combinations, and get suggestions based on your preferences and the weather.

## Shiny app

Run the Shiny app locally from the project root:

```sh
make app
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

Required runtime configuration is loaded from Doppler. Keep only bootstrap values in `.env`:

- `APP_ENV`
- `DOPPLER_TOKEN`

Store application secrets in Doppler.

## Supabase

Database schema changes live in `supabase/migrations/`.

Install the Supabase and Doppler CLIs on macOS:

```sh
brew install supabase/tap/supabase
brew install dopplerhq/cli/doppler
supabase login
```

Use separate Supabase projects for local development and production. Store environment-specific Supabase values in Doppler configs.

To run database commands with values from Doppler:

```sh
doppler run -- make supabase-plan
doppler run -- make supabase-apply
```

To apply pending migrations without Doppler, pass `PROJECT_REF` directly:

```sh
make supabase-plan PROJECT_REF=<project-ref>
make supabase-apply PROJECT_REF=<project-ref>
```

Only use seed data for development or testing:

```sh
make supabase-apply SEED=1
```

To rebuild a throwaway development database from scratch:

```sh
make supabase-reset
```
