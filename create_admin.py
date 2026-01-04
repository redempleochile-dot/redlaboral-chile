import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal_empleos.settings")
django.setup()

from django.contrib.auth import get_user_model

def crear_jefe():
    User = get_user_model()
    username = "SuperJefe"
    password = "Jefe2026"
    email = "admin@chile.cl"

    print("--- INICIANDO PROCESO DE SUPERUSUARIO ---")

    try:
        if not User.objects.filter(username=username).exists():
            print(f"Creando usuario nuevo: {username}")
            User.objects.create_superuser(username, email, password)
        else:
            print(f"El usuario {username} ya existe. Forzando nueva clave...")
            u = User.objects.get(username=username)
            u.set_password(password)
            u.is_superuser = True
            u.is_staff = True
            u.save()
        print("--- ¡ÉXITO! USUARIO LISTO ---")
    except Exception as e:
        print(f"--- ERROR: {e} ---")

if __name__ == "__main__":
    crear_jefe()