from gettext import gettext as _

from telegram.ext import filters

TEXT_FILTER = filters.TEXT & ~filters.COMMAND

# Bot constants
CHANNEL_NAME = "pdf2botdev"
SET_LANG = "set_lang"

# Keyboard constants
CANCEL = _("Cancel")
DONE = _("Done")
BACK = _("Back")

# User data constants
FILE_DATA = "file_data"
MESSAGE_DATA = "message_data"

# Payment Constants
PAYMENT = "payment"

# Datastore constants
USER = "User"
LANGUAGE = "language"
