from saga.core.app import create_app
from saga.core.settings import load_settings

if __name__ == '__main__':
    settings = load_settings('settings.json')
    app = create_app(settings)
    app.run()
