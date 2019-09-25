uwsgi --socket :8001 --module=wheatembryoexp.wsgi:application --env=DJANGO_SETTINGS_MODULE=wheatembryoexp.settings.pro --master --buffer-size 22573
