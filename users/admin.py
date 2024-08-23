from django.contrib import admin
from .models import DoctorsProfile, PatientProfile, User

class DoctorsProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username', 'specialization')

class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')
    search_fields = ('user__username', 'date_of_birth')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_patient', 'is_doctor')
    search_fields = ('username', 'email')

admin.site.register(DoctorsProfile, DoctorsProfileAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
admin.site.register(User, UserAdmin)





# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User, DoctorsProfile, PatientProfile

# class DoctorsProfileInline(admin.StackedInline):
#     model = DoctorsProfile
#     can_delete = False
#     verbose_name_plural = 'Doctors Profile'

# class PatientProfileInline(admin.StackedInline):
#     model = PatientProfile
#     can_delete = False
#     verbose_name_plural = 'Patients Profile'

# class UserAdmin(BaseUserAdmin):
#     inlines = (DoctorsProfileInline, PatientProfileInline)
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_patient', 'is_doctor')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     readonly_fields = ('id',)

# admin.site.register(User, UserAdmin)
# admin.site.register(DoctorsProfile)
# admin.site.register(PatientProfile)












# from django.contrib import admin
# from .models import DoctorsProfile, PatientProfile, User

# class DoctorsProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'specialization')
#     search_fields = ('user__username', 'specialization')

# class PatientProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'date_of_birth')
#     search_fields = ('user__username', 'date_of_birth')

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_patient', 'is_doctor')
#     search_fields = ('username', 'email')

# admin.site.register(DoctorsProfile, DoctorsProfileAdmin)
# admin.site.register(PatientProfile, PatientProfileAdmin)
# admin.site.register(User, UserAdmin)




# from django.contrib import admin
# from .models import DoctorsProfile, PatientProfile, User
# # from django.contrib.auth import get_user_model

# # User = get_user_model()
# # for user in User.objects.all():
# #     print(user.username)

# class DoctorsProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'specialization')
#     search_fields = ('user__username', 'specialization')

# class PatientProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'date_of_birth')
#     search_fields = ('user__username', 'date_of_birth')

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'is_patient', 'is_doctor')
#     search_fields = ('username', 'email')

# admin.site.register(DoctorsProfile, DoctorsProfileAdmin)
# admin.site.register(PatientProfile, PatientProfileAdmin)
# admin.site.register(User, UserAdmin)









# from django.contrib import admin
# from .models import DoctorsProfile, PatientProfile, User


# class DoctorsProfileAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',) #creating an id for each of the profile

# admin.site.register(DoctorsProfile, DoctorsProfileAdmin)



# class PatientProfileAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',) #creating an id for each of the profile

# admin.site.register(PatientProfile, PatientProfileAdmin)

# class UserAdmin(admin.ModelAdmin):
#     readonly_fields = ('id',) #creating an id for each of the profile

# admin.site.register(User, UserAdmin)
