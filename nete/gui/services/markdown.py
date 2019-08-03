import random
import re

from mistune import (
    Markdown,
    Renderer,
    InlineGrammar,
    InlineLexer,
)


class CheckboxRenderer(Renderer):
    def checkbox(self, checked, label):
        id = random.randint(0, 1 << 32)
        return (
            '<div>'
            '  <input type="checkbox" id="{id}" onclick="return false" {checked}>'
            '  <label for={id}>{label}</label>'
            '</div>'.format(
                checked='checked' if checked else '',
                id=id,
                label=label,
            ))


class CheckboxInlineLexer(InlineLexer):
    def enable_checkbox(self):
        self.rules.checkbox = re.compile(
            r'^\[(.)\] (.*)$',
            re.M
        )

        self.default_rules.insert(3, 'checkbox')

    def output_checkbox(self, m):
        checkmark = m.group(1)
        label = m.group(2)
        return self.renderer.checkbox(
            checked=(checkmark != ' '),
            label=label)


renderer = CheckboxRenderer()
inline = CheckboxInlineLexer(renderer)
inline.enable_checkbox()
markdown = Markdown(
    renderer=renderer,
    inline=inline)
