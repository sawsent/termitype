from termitype.models.presentation.presentation import Bar, BarStyle

TOP_BAR_MENU = Bar.MULTIPLE(lines=[
    [" ____  ____  ____  __  __  ____  ____  _  _  ____  ____ ", "github.com/sawsent/termitype"],
    ["(_  _)( ___)(  _ \\(  \\/  )(_  _)(_  _)( \\/ )(  _ \\( ___)", ""],
    ["  )(   )__)  )   / )    (  _)(_   )(   \\  /  )___/ )__) ", ""],
    [" (__) (____)(_)\\_)(_/\\/\\_)(____) (__)  (__) (__)  (____)", ""],
    []
], show_outline=True, style=BarStyle.CENTERED(padding=2))

