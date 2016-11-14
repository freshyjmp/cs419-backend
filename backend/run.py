from backend.app import create_app
from backend.views import results
app = create_app()
app.register_blueprint(results)
app.run(host='0.0.0.0')
