from termitype.app.context import AppContext
from termitype.utils.color import Color, color
from termitype.utils.visuals import LOGO, REPO


def shutdown(context: AppContext) -> None:
    if context.settings.show_exit_message:
        show_exit_message()

def show_exit_message() -> None:
    print()
    print(LOGO)
    print()
    print(f"Thanks for using termitype, consider starring the repo on github here: {color(REPO, Color.CYAN)}")
