from django.contrib import admin


from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import User
from django.contrib.auth.admin import UserAdmin


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
   
    list_display = ('name', 'email')
    
    readonly_fields = ('date_joined', )

    def get_form(self, request, obj=None, **kwargs):
    
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)


admin.site.register(User, UserAdmin)
