from django.contrib import admin
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import UserProfile


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserProfile
   
    list_display = ('first_name', 'last_name', 'email')


    def get_form(self, request, obj=None, **kwargs):
    
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


admin.site.register(UserProfile, UserAdmin)
