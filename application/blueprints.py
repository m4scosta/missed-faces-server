def register_blueprints(app):
    from application.apps.person.controllers import person_mod
    from application.apps.detections.controllers import detection_mod
    from application.apps.detectors.controllers import detector_mod
    from application.apps.auth.controllers import auth_mod
    from application.apps.notifications.controllers import notifications_mod
    from application.apps.home.controllers import home_mod

    app.register_blueprint(person_mod)
    app.register_blueprint(detection_mod)
    app.register_blueprint(detector_mod)
    app.register_blueprint(auth_mod)
    app.register_blueprint(notifications_mod)
    app.register_blueprint(home_mod)
