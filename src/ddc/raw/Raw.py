import os
from functools import cached_property

from utils import File, Log

from ddc.core import Level

log = Log('Raw')


class Raw:
    @property
    def file_path(self):
        return os.path.join('data', 'raw.txt')

    @cached_property
    def lines(self):
        return File(self.file_path).read_lines()

    @staticmethod
    def is_generic_line(line):
        if not line:
            return False
        for k in ['not assigned', 'unassigned']:
            if k in line.lower():
                return False
        return True

    @staticmethod
    def is_level1_line(line, _):
        if not Raw.is_generic_line(line):
            return False
        return line.startswith('Class')

    @staticmethod
    def is_level2_line(line, previous_line):
        if not Raw.is_generic_line(line):
            return False
        if Raw.is_level1_line(line, previous_line):
            return False
        if Raw.is_level2_line(previous_line, None):
            return False
        if line[2] != '0':
            return False
        return True

    @staticmethod
    def is_level3_line(line, previous_line):
        if not Raw.is_generic_line(line):
            return False
        if Raw.is_level1_line(line, previous_line):
            return False
        if Raw.is_level2_line(line, previous_line):
            return False

        return True

    def get_lines_by_level(self, func_level_filter):
        lines = self.lines
        lines1 = []
        for i, line in enumerate(lines):
            if func_level_filter(line, lines[i - 1]):
                lines1.append(line)
        return lines1

    def parse(self) -> Level:
        root = Level(0, '000', 'DDC', [])

        level1_idx = {}
        for line in self.get_lines_by_level(Raw.is_level1_line):
            words = line.split(' ')
            code = words[1]
            name = ' '.join(words[3:])
            level1 = Level(1, code, name, [])
            root.children.append(level1)
            level1_idx[code] = level1

        level2_idx = {}
        for line in self.get_lines_by_level(Raw.is_level2_line):
            words = line.split(' ')
            code = words[0]
            name = ' '.join(words[1:])
            level2 = Level(2, code, name, [])
            parent_code = code[:1] + '00'
            parent = level1_idx[parent_code]
            parent.children.append(level2)
            level2_idx[code] = level2

        for line in self.get_lines_by_level(Raw.is_level3_line):
            words = line.split(' ')
            code = words[0]
            name = ' '.join(words[1:])
            level3 = Level(3, code, name, [])
            parent_code = code[:2] + '0'
            parent = level2_idx[parent_code]
            parent.children.append(level3)

        return root
