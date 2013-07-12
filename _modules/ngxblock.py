import os
import sys
import re

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.filter import simplefilter
from pygments.token import Token

from bs4 import BeautifulSoup

_lnk_replacements = {
    '_LNK_B_': '<a href="http://',
    '_LNK_M_': '" target="_blank">',
    '_LNK_E_': '</a>',
    '_LNK__': '_LNK_',
}
_lnk_regex = re.compile('|'.join(_lnk_replacements.keys()))


def _lnk_replace(match):
    return _lnk_replacements[match.group()]


class ngxblock(nodes.Element):
    pass


@simplefilter
def ngx_linker(self, lexer, stream, options):
    for ttype, value in stream:
        value = value.replace('_LNK_', '_LNK__')
        if ttype is Token.Keyword or ttype is Token.Keyword.Namespace:
            value = '_LNK_B_ngx.cc/r/%s_LNK_M_%s_LNK_E_' % (value, value)
        yield ttype, value


class NgxCodeBlock(Directive):
    '''
    This adds .. ngx:: to the source.
    
    .. ngx:: <param>
    
        server {
            server_name domain.tld;
            root /var/www;
        }
    
    <param>: optional
        empty:    No parameter will generate code block as normal
        warn:     Code block will be generated with pink background
    '''

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'warn': directives.flag,
    }

    def run(self):
        node = ngxblock()
        node['code'] = u'\n'.join(self.content)
        node['warn'] = 'warn' in self.arguments
        return [node]


def _format_text(text, warn):
    '''
    This is the magic that does all the tweaking of our code block.
    '''
    lexer = get_lexer_by_name('nginx')
    linker = ngx_linker()
    lexer.add_filter(linker)
    if warn:
        formatter = HtmlFormatter(cssclass='highlight highlight-warn')
    else:
        formatter = HtmlFormatter(cssclass='highlight')
    markup = highlight(text, lexer, formatter)
    return _lnk_regex.sub(_lnk_replace, markup)


def visit_ngxblock(self, node):
    '''
    Adds the pretty formatted code to the page as a node.
    '''
    self.body.append(_format_text(node['code'], node['warn']))
    raise nodes.SkipNode


def setup(app):
    app.add_node(ngxblock, html=(visit_ngxblock, None))
    app.add_directive('ngx', NgxCodeBlock)
    app.add_stylesheet('ngxblock.css')
