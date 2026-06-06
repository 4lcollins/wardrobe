# Wardrobe

Wardrobe is a personal clothing management app that helps you organize, track, and plan your outfits. Easily catalog your Wardrobe, create outfit combinations, and get suggestions based on your preferences and the weather.

## Shiny app

Run the Shiny app locally from the project root:

```sh
shiny run app/main.py
```

Shiny application code lives in `app/`, while backend logic and services live in `src/`.

### Deploy to Posit Connect Cloud
Via the VSCode extension Posit Publisher, create a deployment for the application.

## Apple shortcuts

Apple shortcut scripts live in `/scripts`. These are deployable via shortcuts and the a-Shell iOS app to run python scripts. Due to the limited runtime environment, only limited packages are supported and all packages need to be pip installed in a-Shell.
