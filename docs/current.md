1. Dev
    - docker + traefik +  postgres + whitenoise
2. Production
    - docker + traefik +  postgres + whitenoise
3. Local tests
    - python manage.py runserver django liveserver test case
    but the settings is using whitenoise?

4. ci
    - using whitenoise and collectstatic in order to run 