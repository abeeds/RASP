"""
This module provides the glossary query form
"""

import forms.form_filler as ff

from forms.form_filler import FLD_NM  # for tests

USERNAME = 'username'
PASSWORD = 'password'

FORM_FLDS = [
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


def get_form() -> list:
    return FORM_FLDS


def get_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(FORM_FLDS)


def get_fld_names() -> list:
    return ff.get_fld_names(FORM_FLDS)


def main():
    # print(f'Form: {get_form()=}\n\n')
    print(f'Form: {get_form_descr()=}\n\n')
    # print(f'Field names: {get_fld_names()=}\n\n')


if __name__ == "__main__":
    main()
