from disguise.forms import DisguiseForm

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
