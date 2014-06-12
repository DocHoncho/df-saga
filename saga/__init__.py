from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash
from ttt import parse_xml, count_attrs
from functools import wraps

app = Flask(__name__)
app.config.from_object(__name__)

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


@app.route('/')
def index():
    return render_template('index.html')

def get_sig_attrs(data):
    s = set()
    for sig in data:
        e, rest = sig.split(':', 1)
        for a in rest.split(' '):
            s.add(a)
    return list(s)

@app.route('/test_load/', methods=['GET', 'POST'])
@templated()
def test_load():
    args = {'data': {}, 'err': [], 'counts': None, 'fn': '', 'events': [], 'event_types': []}

    if request.method == 'POST':
        args['fn'] = request.form.get('fn')

        if args['fn']:
            args['data'] = parse_xml(args['fn'])

        for c in args['data']:
            args['data'][c]['sig_attrs'] = get_sig_attrs(args['data'][c]['sigs'])

        args['attrs'], args['counts'] = count_attrs(args['data'])



    return args


