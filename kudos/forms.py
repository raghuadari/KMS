from django.forms import ModelForm, Textarea

from .models import Kudo, User

class KudoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(KudoForm, self).__init__(*args, **kwargs)
        # Making name required
        self.fields['to_user'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['to_user'].label = "To"
        self.fields['title'].label = "Kudo Title"
        self.fields['to_user'].queryset = User.objects.filter(~User(email=user.email))
    class Meta:
        model = Kudo
        fields = ['to_user', 'title', 'description']
        widgets = {
            'description': Textarea(attrs={'cols': 10, 'rows': 5}),
        }



