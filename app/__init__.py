from app.routes import app
from app.extensions import AppJSONEncoder

app.json_encoder = AppJSONEncoder

if __name__ == '__main__':
    app.run(debug=True)
