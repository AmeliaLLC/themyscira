import pybars


def _list_helper(this, options, items):
    result = []
    for item in items:
        result.append(options['fn'](item))
    return result

def render(source, context):
    compiler = pybars.Compiler()
    with open(source) as f:
        contents = f.read()
        template = compiler.compile(unicode(contents))
    output = template(context, helpers={
        'list': _list_helper
    })
    return ''.join(output).encode('UTF-8')

