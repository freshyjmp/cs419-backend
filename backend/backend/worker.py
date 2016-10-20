from backend.app import create_app
from backend.tasks import q

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        q.start('worker')
