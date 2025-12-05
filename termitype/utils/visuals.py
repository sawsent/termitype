from termitype.models.presentation.presentation import Bar, LineStyle

TOP_BAR_MENU = Bar.MULTIPLE(lines=[
    [" ____  ____  ____  __  __  ____  ____  _  _  ____  ____ ", "github.com/sawsent/termitype"],
    ["(_  _)( ___)(  _ \\(  \\/  )(_  _)(_  _)( \\/ )(  _ \\( ___)", ""],
    ["  )(   )__)  )   / )    (  _)(_   )(   \\  /  )___/ )__) ", ""],
    [" (__) (____)(_)\\_)(_/\\/\\_)(____) (__)  (__) (__)  (____)", ""],
    []
], show_outline=True, style=LineStyle.CENTERED(padding=2))

LOGO = \
    " ____  ____  ____  __  __  ____  ____  _  _  ____  ____ " + "\n" + \
    "(_  _)( ___)(  _ \\(  \\/  )(_  _)(_  _)( \\/ )(  _ \\( ___)" + "\n" + \
    "  )(   )__)  )   / )    (  _)(_   )(   \\  /  )___/ )__) " + "\n" + \
    " (__) (____)(_)\\_)(_/\\/\\_)(____) (__)  (__) (__)  (____)" + "\n"

REPO = "https://www.github.com/sawsent/termitype"
