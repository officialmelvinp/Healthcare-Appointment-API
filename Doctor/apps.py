from django.apps import AppConfig

class DoctorConfig(AppConfig):
    # Sets the default auto field type for primary keys in your models
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Specifies the name of the app, which should match the directory name
    name = 'Doctor'
