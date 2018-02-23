from django.forms import ModelForm, Textarea

from .models import Kudo

class KudoForm(ModelForm):
    class Meta:
        model = Kudo
        fields = ['to_user', 'title', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 10}),
        }

