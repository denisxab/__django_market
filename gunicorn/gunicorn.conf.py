
reload=True # Для продакшина лучше False
command = "/home/denis/PycharmProjects/testvpn/venv/bin/gunicorn"
pythonpath = "/home/denis/PycharmProjects/testvpn/experement/experement"
bind = "unix:/home/denis/PycharmProjects/testvpn/experement/gunicorn/gunicorn.sock"
workers = 3
user = "denis"
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = ["DJANGO_SETTINGS_MODULE=experement.settings",]
accesslog = "/home/denis/PycharmProjects/testvpn/experement/gunicorn/gunicorn_access.log"
errorlog = "/home/denis/PycharmProjects/testvpn/experement/gunicorn/gunicorn_error.log"
	