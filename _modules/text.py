from docutils import nodes


def text_role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
    '''
    Simple role to allow the use of :txt:`plain text` to bypass formatting.
    '''
    node = nodes.raw('', text, format='html')
    return [node], []


def setup(app):
    app.add_role('txt', text_role)
