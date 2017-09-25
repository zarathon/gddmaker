from django.contrib import admin
from django import forms
from .models import Game, Level, Character, Media, Mechanic


class GameAdminForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = '__all__'


class GameAdmin(admin.ModelAdmin):
    form = GameAdminForm
    list_display = ['created', 'last_updated', 'name', 'description']
    readonly_fields = ['created', 'last_updated', 'name', 'description']

admin.site.register(Game, GameAdmin)


class LevelAdminForm(forms.ModelForm):

    class Meta:
        model = Level
        fields = '__all__'


class LevelAdmin(admin.ModelAdmin):
    form = LevelAdminForm
    list_display = ['name', 'description', 'script', 'created', 'last_updated']
    readonly_fields = ['name', 'description', 'created', 'last_updated']

admin.site.register(Level, LevelAdmin)


class CharacterAdminForm(forms.ModelForm):

    class Meta:
        model = Character
        fields = '__all__'


class CharacterAdmin(admin.ModelAdmin):
    form = CharacterAdminForm
    list_display = ['name', 'description', 'created', 'last_updated']
    readonly_fields = ['name', 'description', 'created', 'last_updated']

admin.site.register(Character, CharacterAdmin)


class MediaAdminForm(forms.ModelForm):

    class Meta:
        model = Media
        fields = '__all__'


class MediaAdmin(admin.ModelAdmin):
    form = MediaAdminForm
    list_display = ['name', 'description', 'created', 'last_updated', 'url', 'file', 'type']
    readonly_fields = ['name', 'description', 'created', 'last_updated', 'url', 'file', 'type']

admin.site.register(Media, MediaAdmin)


class MechanicAdminForm(forms.ModelForm):

    class Meta:
        model = Mechanic
        fields = '__all__'


class MechanicAdmin(admin.ModelAdmin):
    form = MechanicAdminForm
    list_display = ['name', 'description', 'created', 'last_updated']
    readonly_fields = ['name', 'description', 'created', 'last_updated']

admin.site.register(Mechanic, MechanicAdmin)


