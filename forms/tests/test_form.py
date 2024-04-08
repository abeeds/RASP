"""
Tests for forms/form.py.
"""
import forms.form as fm


def test_get_form():
    form = fm.get_form()
    assert isinstance(form, list)
    assert len(form) > 0
    for fld in form:
        # Every field must have a name!
        assert 'fieldName' in fld
        # And it can't be blank.
        assert len(fld['fieldName']) > 0


def test_get_form_descr():
    assert isinstance(fm.get_form_descr(), dict)


def test_get_fld_names():
    assert isinstance(fm.get_fld_names(), list)
