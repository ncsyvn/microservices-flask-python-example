from auth_app.app import create_app

app = create_app()
if __name__ == '__main__':
    """
    Main Auth Application
    python manage.py
    """
    app.run(host='0.0.0.0', port=5012)
