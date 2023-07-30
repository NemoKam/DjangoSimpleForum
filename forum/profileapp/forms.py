from django import forms

from profileapp.models import ProfileUser, Post, Comment

from datetime import date

#forms
class UserProfileRegisterForm(forms.ModelForm):

    #Adding class attributes and placeholders to model fields 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            visible.field.widget.attrs['required'] = 'required'
        
        self.fields['gender'].widget.attrs['class'] = 'uk-select'
        self.fields['birthday'].widget.attrs['placeholder'] = 'MM/DD/YYYY'
        self.fields['avatar'].widget.attrs.pop('required')
    
    class Meta:
        model = ProfileUser
        fields = ('birthday', 'gender', 'avatar', 'about')

        widgets = {
           'birthday': forms.DateInput(),
        }

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        try:
            timedlt = date.today() - birthday
        except:
            raise forms.ValidationError('Incorrect Birthday')
        if timedlt.days // 365.2425 >= 18:
            return birthday
        else:
            raise forms.ValidationError('Your age is under 18')

    def save(self, user_id):
        new_profile = ProfileUser.objects.get(id=user_id)
        new_profile.birthday = self.cleaned_data['birthday']
        new_profile.gender = self.cleaned_data['gender']
        new_profile.avatar = self.cleaned_data['avatar']
        new_profile.about = self.cleaned_data['about']
        new_profile.save()

class PostCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            visible.field.widget.attrs['required'] = 'required'
        
        self.fields['img'].widget.attrs.pop('required')

    class Meta:
        model = Post
        fields = ('text', 'img')

    def save(self, user, post_id: None):
        post = ''
        if post_id:
            post = Post.objects.get(id=post_id)
            if self.cleaned_data['img']:
                post.img = self.cleaned_data['img']
            else:
                post.img = ''
            post.text = self.cleaned_data['text']
        else:
            if self.cleaned_data['img']:
                post = Post.objects.create(author=user, text=self.cleaned_data['text'], img=self.cleaned_data['img'])
            else:
                post = Post.objects.create(author=user, text=self.cleaned_data['text'])
        post.save()
        return post

class CommentCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input comments_inp'
            visible.field.widget.attrs['placeholder'] = visible.field.label
            visible.field.widget.attrs['required'] = 'required'
        
        self.fields['img'].widget.attrs.pop('required')
        self.fields['img'].widget.attrs['class'] = 'uk-input'

    class Meta:
        model = Comment
        fields = ('text', 'img')

    def save(self, post_id, user):
        new_post = Post.objects.get(id=post_id).comments.create(author=user, text=self.cleaned_data['text'], img=self.cleaned_data['img'])
        new_post.save()