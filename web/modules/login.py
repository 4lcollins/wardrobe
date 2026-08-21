from shiny import module, reactive, render, ui

from src.db.users import get_user_by_email


LOGIN_ART = [
    {
        "src": "assets/apparel-sweater-sage.png",
        "alt": "Sage sweater",
    },
    {
        "src": "assets/apparel-sweater-cream.png",
        "alt": "Cream sweater",
    },
    {
        "src": "assets/apparel-tshirt-clay.png",
        "alt": "Clay t-shirt",
    },
    {
        "src": "assets/apparel-blouse-cream.png",
        "alt": "Cream blouse",
    },
    {
        "src": "assets/apparel-sweater-gray.png",
        "alt": "Gray sweater",
    },
]


class LoginState:
    def __init__(self, current_user, login_error_message):
        self.current_user = current_user
        self.login_error_message = login_error_message

    def get_user(self):
        return self.current_user.get()

    def clear(self):
        self.current_user.set(None)
        self.login_error_message.set(None)


@module.ui
def login_ui():
    return ui.div(
        ui.div(
            ui.div(
                ui.input_dark_mode(
                    id="theme_mode",
                ),
                class_="theme-control login-theme-control",
            ),
            ui.output_ui("login_art"),
            ui.h1(
                "Wardrobe",
                class_="hero-header",
            ),
            ui.p(
                "Your cozy outfit guide",
                class_="hero-kicker",
            ),
            class_="login-hero hero-panel",
        ),
        ui.div(
            ui.div(
                ui.h2(
                    "Login",
                    class_="panel-title",
                ),
                ui.output_ui("login_error"),
                ui.input_text(
                    "login_email",
                    "Email",
                    placeholder="you@example.com",
                ),
                ui.input_action_button(
                    "login_btn",
                    "Sign In",
                    class_="btn btn-primary game-button w-100",
                ),
                class_="login-card game-panel",
            ),
            class_="login-card-wrap",
        ),
        class_="app-shell login-shell",
    )


@module.server
def login_server(input, output, session):
    current_user = reactive.Value(None)
    login_error_message = reactive.Value(None)
    art_index = reactive.Value(1)

    def _shift_art(offset: int):
        art_index.set((art_index.get() + offset) % len(LOGIN_ART))

    @reactive.effect
    @reactive.event(input.previous_art_btn)
    def _previous_art():
        _shift_art(-1)

    @reactive.effect
    @reactive.event(input.next_art_btn)
    def _next_art():
        _shift_art(1)

    @reactive.effect
    @reactive.event(input.login_btn)
    def _handle_login():
        email = input.login_email()

        try:
            user = get_user_by_email(email)
        except Exception:
            login_error_message.set("Login is temporarily unavailable. Try again soon.")
            return

        if not user:
            login_error_message.set("We couldn't sign you in with that email.")
            return

        current_user.set(user)
        login_error_message.set(None)

    @output
    @render.ui
    def login_error():
        message = login_error_message.get()

        if not message:
            return ui.div()

        return ui.div(message, class_="game-alert login-alert")

    @output
    @render.ui
    def login_art():
        current = art_index.get()
        previous_art = LOGIN_ART[(current - 1) % len(LOGIN_ART)]
        current_art = LOGIN_ART[current]
        next_art = LOGIN_ART[(current + 1) % len(LOGIN_ART)]

        return ui.div(
            ui.input_action_button(
                "previous_art_btn",
                ui.div(
                    ui.span("‹", class_="login-art-arrow"),
                    ui.img(
                        src=previous_art["src"],
                        alt=previous_art["alt"],
                        class_="login-art-item login-art-side",
                    ),
                    class_="login-art-side-wrap",
                ),
                class_="login-art-button",
            ),
            ui.img(
                src=current_art["src"],
                alt=current_art["alt"],
                class_="login-art-item login-art-feature",
            ),
            ui.input_action_button(
                "next_art_btn",
                ui.div(
                    ui.img(
                        src=next_art["src"],
                        alt=next_art["alt"],
                        class_="login-art-item login-art-side",
                    ),
                    ui.span("›", class_="login-art-arrow"),
                    class_="login-art-side-wrap",
                ),
                class_="login-art-button",
            ),
            class_="login-art-row",
        )

    return LoginState(current_user, login_error_message)
