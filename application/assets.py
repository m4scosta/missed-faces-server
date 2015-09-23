from flask.ext.assets import Bundle, Environment

bundles = {
    'home_js': Bundle('test.js', 'home.js', output='gen/home.js', filters='jsmin')
}


def register_assets(app):
    assets = Environment(app)
    assets.register(bundles)
