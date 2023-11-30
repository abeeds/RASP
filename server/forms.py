TITLE = 'Title'
TYPE = 'Type'
FORM = "Form"
DATA = 'Data'


PROMPT = "Prompt"
VALUE = "Value"
FLDS = "Fields"
HIVAL = "Hival"
LOWVAL = "Lowval"

# Types of form data:
INT = "INT"
STR = "STR"

USERNAME = "username"
PASSWORD = "password"

RETURN = 'Return'
MENU = 'menu'


USERNAME_FORM = {
    TITLE: "Username",
    TYPE: FORM,
    FLDS: {
        USERNAME: {
            VALUE: "",
            PROMPT: "Please enter your username",
            TYPE: STR
        }
    },
}


PASSWORD_FORM = {
    TITLE: "Password",
    TYPE: FORM,
    FLDS: {
        PASSWORD: {
            VALUE: "",
            PROMPT: "Please enter your password",
            TYPE: STR
        }
    },
}
