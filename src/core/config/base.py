import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) + os.sep
TEMPLATE_DIR = BASE_DIR + "src" + os.sep + "templates" + os.sep

# Postgresql
# You need set this environment variables:
# DB = {
#     "DIALECT": os.getenv("DB_DIALECT", "postgresql+psycopg2"),
#     "HOST": os.getenv("DB_HOST"),
#     "PORT": os.getenv("DB_PORT"),
#     "NAME": os.getenv("DB_NAME"),
#     "USER": os.getenv("DB_USER"),
#     "PASSWORD": os.getenv("DB_PASSWORD"),
# }

# app settings
ROOMS = {
    "97.1": {"places": 14},
    "90": {"places": 21},
}

COLORS = {
    "green": "#00FF00",
    "gold": "#FFFF00",
    "red": "#FF0000",
}


TIME = [
    "00:00",
    "00:30",
    "01:00",
    "01:30",
    "02:00",
    "02:30",
    "03:00",
    "03:30",
    "04:00",
    "04:30",
    "05:00",
    "05:30",
    "06:00",
    "06:30",
    "07:00",
    "07:30",
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30",
    "22:00",
    "22:30",
    "23:00",
    "23:30",
]


STREAMLIT_STYLES = """ <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto');
    html, body, [class*="css"]  {
    font-family: 'Roboto', sans;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style> """



# Oauth
    # Application (client) ID of app registration
    # managed in  https://aad.portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/RegisteredApps page
# CLIENT_ID = os.getenv("CLIENT_ID") 

 # Application (client) secret of app registration
# CLIENT_SECRET = os.getenv("CLIENT_SECRET") 


# REDIRECT_URI = ""
# TENANT = os.getenv('TENANT')

# LOGOUT_URL = f"https://login.microsoftonline.com/{TENANT}/oauth2/v2.0/logout?post_logout_redirect_uri={REDIRECT_URI}"

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
# SCOPE = ["User.Read"]