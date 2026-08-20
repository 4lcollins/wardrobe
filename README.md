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

To copy the project to iCloud Drive for Apple Shortcuts/a-Shell workflows:

```sh
make deploy
```

Shortcut runner code lives in `shortcuts/`. Keep that environment lightweight; a-Shell supports only a limited Python package set.
