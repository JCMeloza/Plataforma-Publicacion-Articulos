from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets

from articles.models import Article, Category, Comment, Tag
from editorial.models import Review

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

class ChangeRoleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']


#Formulario para crear una publicación (renamed from ReviewCreateForm)
class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = [
            'title',
            'content',
            'image',
            'category',
            'tags'
        ]


# Backward compatibility alias (deprecated: use ArticleForm)
ReviewCreateForm = ArticleForm

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comments', 'feedback']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Comentarios internos (requerido)...'}),
            'feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Sugerencias para el autor (opcional)...'}),
        }
        labels = {
            'comments': 'Comentarios internos *',
            'feedback': 'Sugerencias para el autor',
        }

    def __init__(self, *args, **kwargs):
        self.decision = kwargs.pop('decision', None)
        super().__init__(*args, **kwargs)
        if self.decision:
            self.instance.decision = self.decision


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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'class' : 'comment-textarea',
                'placeholder': 'Escribe tu comentario aquí...'
            }),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        #  Sincronizados: Eliminamos 'role' por seguridad y añadimos 'email'
        fields = ['username', 'email', 'bio', 'avatar'] 
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'comment-textarea'}),
            'email': forms.EmailInput(attrs={'class': 'comment-textarea'}),
            'bio': forms.Textarea(attrs={'class': 'comment-textarea', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-file-input'}),
        }