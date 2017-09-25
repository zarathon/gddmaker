from django import forms
from .models import Game, Level, Character, Media, Mechanic


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = ['name', 'description', 'script', 'characters', 'medias', 'mechanics']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'script': 'Roteiro',
            'characters': 'Personagens',
            'medias': 'Mídias',
            'mechanics': 'Mecânicas'
        }

    def __init__(self, *args, **kwargs):
        game = kwargs.pop("game")
        super(LevelForm, self).__init__(*args, **kwargs)
        self.fields["characters"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields[
            "characters"].help_text = "Selecione os personagens que fazem parte dessa fase, caso falte alguma, crie e edite sua fase."
        self.fields["characters"].queryset = Character.objects.filter(game=game)
        self.fields["medias"].widget = forms.widgets.CheckboxSelectMultiple(attrs={'class': 'checkbox-inline'})
        self.fields[
            "medias"].help_text = "Selecione as mídias que fazem parte dessa fase, caso falte alguma, crie e edite sua fase."
        self.fields["medias"].queryset = Media.objects.filter(game=game)
        self.fields["mechanics"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields[
            "mechanics"].help_text = "Selecione as mecânicas que fazem parte dessa fase, caso falte alguma, crie e edite sua fase."
        self.fields["mechanics"].queryset = Mechanic.objects.filter(game=game)


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'description', 'medias', 'mechanics']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'medias': 'Mídias',
            'mechanics': 'Mecânicas'
        }

    def __init__(self, *args, **kwargs):
        game = kwargs.pop("game")
        super(CharacterForm, self).__init__(*args, **kwargs)
        self.fields["medias"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields[
            "medias"].help_text = "Selecione as que tem ligação com seu personagem, caso falte alguma, crie e edite seu personagem."
        self.fields["medias"].queryset = Media.objects.filter(game=game)
        self.fields["mechanics"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields[
            "mechanics"].help_text = "Selecione as que tem ligação com seu personagem, caso falte alguma, crie e edite seu personagem."
        self.fields["mechanics"].queryset = Mechanic.objects.filter(game=game)


class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['name', 'description', 'type', 'url', 'file' ]
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'file': 'Arquivo',
            'type': 'Tipo'
        }
        help_texts = {
            'type': "Escolha o tipo de mídia que você deseja, caso deseje Audio ou Picture, você deverá enviar um arquivo ou adicionar uma url que contenha o conteúdo desejado, caso escolha Video, você deverá a URL do vídeo (Youtube ou Vimeo)."
        }


class MechanicForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['name', 'description', 'medias']
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'medias': 'Mídias'
        }

    def __init__(self, *args, **kwargs):
        game = kwargs.pop("game")
        super(MechanicForm, self).__init__(*args, **kwargs)
        self.fields["medias"].widget = forms.widgets.CheckboxSelectMultiple(attrs={'class': 'checkbox-inline'})
        self.fields[
            "medias"].help_text = "Selecione as mídias que fazem parte dessa fase, caso falte alguma, crie e edite sua fase."
        self.fields["medias"].queryset = Media.objects.filter(game=game)
