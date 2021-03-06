# -*- coding: utf-8 -*-
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import User, UserProfile


class UserForm(forms.ModelForm):
    """
    Edit username
    """
    def clean_username(self):
        if self.initial['username'] == self.cleaned_data['username']:
            raise forms.ValidationError(
                _("Please choose a different username."))
        try:
            User.objects.get(username=self.cleaned_data['username'])
            raise ValidationError(
                _('A user with that username already exists.'))
        except User.DoesNotExist:
            pass
        return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ['username']


class UserProfileForm(forms.ModelForm):
    """
    Edit user profile
    """
    # avatar = forms.ImageField(required=False) # TODO
    name = forms.CharField(label=_('Name'), required=False, max_length=255)
    location = forms.CharField(label=_('Location'),
                               required=False, max_length=255)
    website = forms.CharField(label=_('Website'),
                              required=False, max_length=255)
    bio = forms.CharField(label=_('About me'),
                          required=False,
                          widget=forms.Textarea())

    helper = FormHelper()
    helper.form_class = 'users-update'
    helper.form_action = 'users:update'
    helper.layout = Layout(
        # 'avatar', # TODO
        'name',
        'location',
        'website',
        HTML('<label for="id_status" class="control-label ">'),
        HTML(_('Occupation')),
        HTML('</label>'),
        Div('student', 'assistant', 'professional', 'professor',
            css_class='users-update-status'),
        Field('bio', rows="3", css_class='input-xlarge'),
        FormActions(
            Submit('submit', _('Update Profile'), css_class="btn-primary"),
        ),
    )

    class Meta:
        model = UserProfile
        exclude = ['user', 'avatar']


DELETE_CONFIRMATION_PHRASE = _('delete my account')


class UserDeleteForm(forms.ModelForm):

    confirmation_phrase_en = _('To verify, type "<span class='
                               '"confirmation-phrase do-not-copy-me">'
                               'delete my account</span>" below:')
    form_labels = {
        'sudo_login': _('Your username or email:'),
        'confirmation_phrase': confirmation_phrase_en,
        'sudo_password': _('Confirm your password:'),
    }

    sudo_login = forms.CharField(
        label=form_labels['sudo_login'],
        required=True,
        max_length=255
    )
    confirmation_phrase = forms.CharField(
        label=form_labels['confirmation_phrase'],
        required=True,
        max_length=255
    )
    sudo_password = forms.CharField(
        label=form_labels['sudo_password'],
        required=True,
        max_length=128,
        widget=forms.PasswordInput
    )

    helper = FormHelper()
    helper.form_class = 'users-delete'
    helper.form_action = 'users:account'
    helper.layout = Layout(
        Field('sudo_login', css_class='form-control'),
        Field('confirmation_phrase', css_class='form-control'),
        Field('sudo_password', css_class='form-control'),
        FormActions(
            Submit('submit_delete', _('Delete your account'),
                   css_class="btn btn-danger"),
        ),
    )

    def clean_sudo_login(self):
        login = self.cleaned_data.get("sudo_login")
        if login != self.user.username and login != self.user.email:
            raise forms.ValidationError(_("The login and/or password you "
                                          "specified are not correct."))
        return self.cleaned_data["sudo_login"]

    def clean_confirmation_phrase(self):
        confirmation_phrase = self.cleaned_data.get("confirmation_phrase")
        if str(DELETE_CONFIRMATION_PHRASE) != confirmation_phrase:
            raise forms.ValidationError(
                _("Confirmation phrase is not correct."))
        return self.cleaned_data["confirmation_phrase"]

    def clean_sudo_password(self):
        password = self.cleaned_data.get("sudo_password")
        if not self.user.check_password(password):
            raise forms.ValidationError(_("The login and/or password you "
                                          "specified are not correct."))
        return self.cleaned_data["sudo_password"]

    def is_valid(self):
        self.user = self.instance
        return super(UserDeleteForm, self).is_valid()

    class Meta:
        model = User
        fields = []
