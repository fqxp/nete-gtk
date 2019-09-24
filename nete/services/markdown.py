import random
import re

from mistune import (
    BlockGrammar,
    BlockLexer,
    Markdown,
    Renderer,
)


class CheckboxRenderer(Renderer):
    def checkbox(self, level, checked, label):
        id = random.randint(0, 1 << 32)
        return (
            '<div class="checkbox checkbox__level_{level}">'
            '  <input type="checkbox" id="{id}" onclick="return false" {checked}>'
            '  <label for="{id}">{label}</label>'
            '</div>'.format(
                level=level + 1,
                checked='checked' if checked else '',
                id=id,
                label=label,
            ))


class CheckboxGrammar(BlockGrammar):

    checkbox = re.compile(r'^( *)\[(.)\] (.*?)(?:\n+|$)', re.M)


class CheckboxBlockLexer(BlockLexer):

    grammar_class = CheckboxGrammar

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enable_checkbox()

    def enable_checkbox(self):
        self.default_rules.insert(0, 'checkbox')

    def parse_checkbox(self, m):
        self.tokens.append({
            'type': 'checkbox',
            'level': m.group(1),
            'checked': m.group(2),
            'label': m.group(3),
        })


class CustomMarkdown(Markdown):
    def output_checkbox(self):
        level = int(len(self.token['level']) / 2)
        checked = self.token['checked'] != ' '
        label = self.token['label']

        return self.renderer.checkbox(level, checked, label)


renderer = CheckboxRenderer()
lexer = CheckboxBlockLexer()
markdown = CustomMarkdown(renderer=renderer, block=lexer)
