from coderedcms.blocks import BaseBlock
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from wagtail.core import blocks


class CodeBlock(BaseBlock):
    """
    Source code with syntax highlighting in a <pre> tag.
    """
    LANGUAGE_CHOICES = []

    for lex in get_all_lexers():
        LANGUAGE_CHOICES.append((lex[1][0], lex[0]))

    language = blocks.ChoiceBlock(
        required=False,
        choices=LANGUAGE_CHOICES,
        label=_('Syntax highlighting'),
    )
    title = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_('Title'),
    )
    code = blocks.TextBlock(
        classname='monospace',
        rows=8,
        label=('Code'),
        help_text=_('Code is rendered in a <pre> tag.'),
    )

    def get_context(self, value, parent_context=None):
        ctx = super(CodeBlock, self).get_context(value, parent_context)

        if value['language']:
            src = value['code'].strip('\n')
            lexer = get_lexer_by_name(value['language'])
            code_html = mark_safe(highlight(src, lexer, HtmlFormatter()))
        else:
            code_html = format_html('<pre>{}</pre>', value['code'])

        ctx.update({
            'code_html': code_html,
        })

        return ctx

    class Meta:
        template = 'coderedcms/blocks/code_block.html'
        icon = 'fa-file-code-o'
        label = _('Formatted Code')
