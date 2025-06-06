#root/main.py
import os

from flask import Flask

from src.configs.app import Config, create_app
from src.controllers.auth_controller import auth_bp
from src.controllers.criminal_controller import criminal_bp
from src.controllers.dashboard_controller import dashboard_bp
from src.controllers.identification_controller import identification_bp
from src.controllers.missing_controller import missing_bp


def main():
    # Custom error handling
    error_handlers = []
    # import torch
    # print("this is: ",torch.cuda.is_available())

    # Blueprints
    blueprints = [identification_bp, criminal_bp,
                  dashboard_bp, missing_bp, auth_bp]

    # Set static folder to the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_folder = os.path.join(current_dir, 'static')
    template_folder = os.path.join(current_dir, 'src', 'templates')

    # Make sure the uploads and static directories exist
    os.makedirs(static_folder, exist_ok=True)
    os.makedirs(template_folder, exist_ok=True)

    # Load configuration
    config = Config()
    flask_app = Flask(__name__,
                template_folder=template_folder,
                static_folder=static_folder
    )

    app = create_app(
        flask_app,
        config,
        blueprints=blueprints,
        error_handlers=error_handlers
    )

    try:
        options = {
            "host":  config.getConfig()["server"]["ip"],
            "port":  config.getConfig()["server"]["port"],
            "debug": config.getConfig()["server"]["debug"]
        }

        app.run(**options)

    except KeyError as e:
        print(f"Configuration error: Missing {e} in the configuration.")
        exit(1)


if __name__ == '__main__':
    main()
