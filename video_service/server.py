from video_app.app import create_app

app = create_app()
if __name__ == '__main__':
    """
    Main Video Application
    python manage.py
    """
    app.run(host='0.0.0.0', port=5013)
