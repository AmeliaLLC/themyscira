import pybars


HELPERS = {}
PARTIALS = {
    'navigation': pybars.Compiler().compile(open('templates/navigation.handlebars').read().decode('UTF-8'))
}

def render(source, context, use_base=True):
    compiler = pybars.Compiler()

    with open(source) as f:
        template_contents = unicode(f.read().decode('utf-8'))
    template = compiler.compile(template_contents)

    if use_base:
        with open('templates/base.handlebars') as f:
            main_contents = f.read().decode('utf-8')
        main_template = compiler.compile(main_contents)
        partials = dict(PARTIALS, content=template)
        output = main_template(
            context, helpers=HELPERS, partials=partials)
    else:
        output = template(context, helpers=HELPERS)

    return ''.join(output).encode('UTF-8')
