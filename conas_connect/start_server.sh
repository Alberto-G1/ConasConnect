# #!/bin/bash

# echo "Starting Conas Connect Server..."
# echo "================================"

# # Check if virtual environment exists
# if [ ! -d "venv" ]; then
#     echo "Creating virtual environment..."
#     python -m venv venv
# fi

# # Activate virtual environment
# source venv/bin/activate

# # Install requirements
# echo "Installing requirements..."
# pip install -r requirements.txt

# # Run migrations
# echo "Running migrations..."
# python manage.py makemigrations
# python manage.py migrate

# # Setup initial data
# echo "Setting up initial data..."
# python manage.py setup_initial_data

# # Collect static files
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# # Create superuser if needed
# echo "Creating superuser (if needed)..."
# python manage.py shell -c "
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
#     print('Superuser created: admin/admin123')
# else:
#     print('Superuser already exists')
# "

# echo "================================"
# echo "🚀 Starting development server..."
# echo "Visit: http://127.0.0.1:8000"
# echo "Admin: http://127.0.0.1:8000/admin"
# echo "Login: admin/admin123"
# echo "================================"

# python manage.py runserver
