# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from index import models
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = models.UserProfile
        fields = ('email','name')
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        #self.instance.username = self.cleaned_data.get('email')
        #password_validation.validate_password(self.cleaned_data.get['password2'],self.instance)
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name','is_active', 'is_superuser')
    def clean_password(self):
        return self.initial["password"]
class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'name','is_superuser', 'is_active')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Personal info', {'fields': ('name')}),
        ('Permissions', {'fields': ('is_active','is_superuser', )}),
        ('有权限操作的主机或主机组', {'fields': ('bind_hosts', 'host_groups')}),
        ('用户其它权限', {'fields': ('user_permissions',)}),
        ('账户有效期', {'fields': ('valid_begin_time', 'valid_end_time')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','name')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('bind_hosts', 'user_permissions', 'groups')


admin.site.register(models.UserProfile)
