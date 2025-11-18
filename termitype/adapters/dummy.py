from termitype.adapters.base import Adapter
from typing import override

class DummyAdapter(Adapter):

    def __init__(self):
        pass

    @override
    def render(self, text: str):
        print(text)

    @override
    def get_key(self) -> str:
        ret = input("Press a key and enter: ")
        return ret

    @override
    def clear(self):
        pass

    @override
    def finalize(self):
        pass
