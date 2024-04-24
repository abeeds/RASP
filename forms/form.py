"""
This module provides the glossary query form
"""

import forms.form_filler as ff

from forms.form_filler import FLD_NM  # for tests

USERNAME = 'username'
PASSWORD = 'password'
FIELDNM = 'fieldName'
TYPE = 'type'
LABEL = 'label'

FORM_FLDS0 = [
    {
        FLD_NM: 'Instructions',
        ff.QSTN: 'Leave all fields blank to see all glossary entries.',
        ff.INSTRUCTIONS: True,
    },
    {
        FLD_NM: USERNAME,
        ff.QSTN: 'Username:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        FLD_NM: PASSWORD,
        ff.QSTN: 'Password:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
]


FORM_FLDS = [
    {
        FIELDNM: 'user',
        TYPE: 'text',
        LABEL: 'Confirm User'
    },
    {
        FIELDNM: 'oldpwd',
        TYPE: 'password',
        LABEL: 'Old Password'
    },
    {
        FIELDNM: 'newpwd',
        TYPE: 'password',
        LABEL: 'New Password'
    },
    {
        FIELDNM: 'newpwdConfirm',
        TYPE: 'password',
        LABEL: 'Confirm Password'
    },
]


FORMS = {
    "UpdatePass": [
        {
            FIELDNM: 'user',
            TYPE: 'text',
            LABEL: 'Confirm User'
        },
        {
            FIELDNM: 'oldpwd',
            TYPE: 'password',
            LABEL: 'Old Password'
        },
        {
            FIELDNM: 'newpwd',
            TYPE: 'password',
            LABEL: 'New Password'
        },
        {
            FIELDNM: 'newpwdConfirm',
            TYPE: 'password',
            LABEL: 'Confirm Password'
        },
    ],
    "FormB": [
        {
            FIELDNM: 'user',
            TYPE: 'text',
            LABEL: 'Confirm User'
        },
        {
            FIELDNM: 'color',
            TYPE: 'color',
            LABEL: 'form b'
        },
    ],
}


def get_form() -> list:
    return FORM_FLDS


def fetch_form(formName) -> list:
    return FORMS[formName]


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(FORM_FLDS0)


def get_fld_names() -> list:
    return ff.get_fld_names(FORM_FLDS0)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()
