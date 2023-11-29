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


REGISTRATION = {
    TITLE: "Registration",
    TYPE: FORM,
    FLDS: {
        USERNAME: {
            VALUE: "",
            PROMPT: "Please enter a username",
            TYPE: STR
        },
        PASSWORD: {
            VALUE: "",
            PROMPT: "Please enter a password",
            TYPE: STR
        },
    }
}

LOGIN = {
    TITLE: "Log In",
    TYPE: FORM,
    FLDS: {
        USERNAME: {
            VALUE: "",
            PROMPT: "Please enter your username",
            TYPE: STR
        },
        PASSWORD: {
            VALUE: "",
            PROMPT: "Please enter your password",
            TYPE: STR
        },
    }
}
