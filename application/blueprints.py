def register_blueprints(app):
    from application.apps.person.controllers import person_mod
    from application.apps.detections.controllers import detection_mod
    from application.apps.detectors.controllers import detector_mod

    app.register_blueprint(person_mod)
    app.register_blueprint(detection_mod)
    app.register_blueprint(detector_mod)
