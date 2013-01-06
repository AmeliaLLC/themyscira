import pybars


def _list_helper(this, options, items):
    result = []
    for item in items:
        result.append(options['fn'](item))
    return result

HELPERS = {
    'list': _list_helper
}

def render(source, context, use_base=True):
    compiler = pybars.Compiler()

    with open(source) as f:
        template_contents = unicode(f.read())
    template = compiler.compile(template_contents)

    if use_base:
        with open('templates/base.handlebars') as f:
            main_contents = f.read().decode('utf-8')
        main_template = compiler.compile(main_contents)
        output = main_template(context, helpers=HELPERS, partials={
            'content': template
        })
    else:
        output = template(context, helpers=HELPERS)

    return ''.join(output).encode('UTF-8')
