from flask import Flask
from flask_cors import CORS
import connexion

app = connexion.App(__name__, specification_dir="./")

app.add_api("swagger.yml")

# add CORS support
CORS(app.app)

if __name__ == "__main__":
    app.run(debug=True)
