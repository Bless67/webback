import os
import django
from django.contrib.auth.models import User
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()



# Check if superuser already exists
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin6110")
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")