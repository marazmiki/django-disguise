from django import forms

from disguise import conf
from disguise.forms import DisguiseForm, get_disguise_form_class


def test_form_invalid_everything():
    form = DisguiseForm({})
    assert not form.is_valid()
    assert '__all__' in form.errors


def test_handle_invalid_username(regular_user):
    form = DisguiseForm({'username': regular_user.username + '_not'})
    assert not form.is_valid()
    assert 'username' in form.errors


def test_handle_invalid_user_id():
    form = DisguiseForm({'user_id': 31337})
    assert not form.is_valid()
    assert 'user_id' in form.errors


def test_handle_valid_username(regular_user):
    form = DisguiseForm({'username': regular_user.username})
    assert form.is_valid()


def test_form_valid_when_correct_user_id(regular_user):
    form = DisguiseForm({'user_id': regular_user.id})
    assert form.is_valid()


def test_get_disguise_form_class():
    assert isinstance(get_disguise_form_class()(), DisguiseForm)


def test_get_disguise_form_class_customized(monkeypatch):
    class MyForm(forms.Form):
        pass
    monkeypatch.setattr(conf, 'CUSTOMIZED_WIDGET_FORM_CLASS', MyForm)
    assert isinstance(get_disguise_form_class()(), MyForm)
