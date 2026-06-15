from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from articles.models import Article, Category, Tag

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class ChangeRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']


#Formulario para crear una publicación
class ReviewCreateForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'image',
            'category',
            'tags'
        ]

#Formulario para crear categorias
class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]

#Formulario para crear una etiqueta
class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'name'
        ]