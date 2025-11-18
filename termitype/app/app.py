from termitype.app.config import AppConfig

class App:

    def __init__(self, config: AppConfig):
        self.adapter = config.adapter
        self.view = config.starting_view

    def run(self):
        while self.view is not None:
            self.view.render()

            key = self.adapter.get_key()
            self.view.handle_input(key)

            self.view = self.view.next_view()
