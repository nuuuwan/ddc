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

    def __str__(self):
        tabs = '  ' * self.level
        return (
            f'{tabs}* {self.code} {self.name}'
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
