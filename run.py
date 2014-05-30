from saga.core.app import create_app, DEFAULT_APP_SETTINGS
from saga.core.settings import load_settings
from werkzeug.serving import run_simple

if __name__ == '__main__':
    from werkzeug.serving import run_simple

    settings = load_settings('settings.json', DEFAULT_APP_SETTINGS)

    app = create_app(settings)
    print(app.hostname, app.port)
    run_simple(app.hostname,
                app.port,
                app,
                use_debugger=app.debug,
                use_reloader=app.reloader)
