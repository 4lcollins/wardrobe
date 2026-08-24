# Wardrobe

Wardrobe is a personal clothing management app that helps you organize, track, and plan your outfits. Easily catalog your Wardrobe, create outfit combinations, and get suggestions based on your preferences and the weather.

## App

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

## Automation

Daily outfit emails run from GitHub Actions in `.github/workflows/daily-outfit.yml`.

Required runtime configuration is loaded from Doppler. Keep only bootstrap values in `.env`:

- `APP_ENV`
- `DOPPLER_TOKEN`

Store application secrets in Doppler.

## Supabase

Database schema changes live in `supabase/migrations/`. Supabase Make targets load `SUPABASE_PROJECT_REF` through Doppler, so both CLIs are required:

- [Supabase CLI install docs](https://supabase.com/docs/guides/local-development/cli/getting-started)
- [Doppler CLI install docs](https://docs.doppler.com/docs/cli)

After installing, authenticate Supabase:

```sh
supabase login
```

Use separate Supabase projects for local development and production. Store environment-specific Supabase values in Doppler.

```sh
make supabase-plan
make supabase-apply
```

Only use seed data for development or testing:

```sh
make supabase-apply SEED=1
```

To rebuild a throwaway development database from scratch:

```sh
make supabase-reset
```
