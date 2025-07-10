file_path="./logs/ims.log"

if [ ! -f "$file_path" ]; then
  mkdir "logs"
  touch "./logs/ims.log"
fi
echo ""

python manage.py runserver 0.0.0.0:8000
