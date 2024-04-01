import os
from dataclasses import dataclass

from utils import File, Log

log = Log('Level')


@dataclass
class Level:
    level: int
    code: str
    name: str
    children: list['Level']

    @property
    def str_self_only(self) -> str:
        tabs = '  ' * self.level
        return f'{tabs}* {self.code} {self.name}'

    def __str__(self):
        return (
            self.str_self_only
            + '\n'
            + ''.join([str(child) for child in self.children])
        )

    def write_md(self):
        assert self.level == 0
        md_path = "README.md"
        lines = ['# Dewey Decimal Classification (ddc)', '', str(self)]
        File(md_path).write_lines(lines)
        log.info(f'Wrote {md_path}')
        os.startfile(md_path)

    def search(self, search_phrase):
        if any(
            [
                search_phrase.lower() in self.name.lower(),
                search_phrase.lower() == self.code.lower(),
            ]
        ):
            print(self)
        for child in self.children:
            child.search(search_phrase)
