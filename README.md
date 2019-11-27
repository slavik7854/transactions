# Run application

1. `sudo docker-compose up -d --no-deps --build --force-recreat`
2. `sudo docker-compose run web python3 manage.py migrate`
3. `sudo docker-compose run web python3 manage.py collectstatic`
4. create a `superuser` (admin) - `sudo docker-compose run web python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"`
5. `sudo docker-compose up`

Site included at http://0.0.0.0:9001/api/

Admin - http://0.0.0.0:9001/admin/

# Instructions

1. Sign In to `admin page`.
2. Create users on the page `/admin/auth/user/`
3. Create accounts and relate their with users on the page `/admin/payment/account/`
4. List of payments and create payment - http://0.0.0.0:9001/api/payment/
5. List of accounts - http://0.0.0.0:9001/api/accounts/


## Run tests

```bash
./manage.py test
```