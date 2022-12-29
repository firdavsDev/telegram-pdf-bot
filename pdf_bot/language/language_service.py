import gettext
from typing import Callable

from telegram import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from pdf_bot.language.language_repository import LanguageRepository


class LanguageService:
    LANGUAGES_KEYBOARD_SIZE = 2
    LANGUAGE = "language"
    LANGUAGE_CODES = {
        "🇬🇧 English (UK)": "en_GB",
        "🇺🇸 English (US)": "en_US",
        "🇭🇰 廣東話": "zh_HK",
        "🇹🇼 繁體中文": "zh_TW",
        "🇨🇳 简体中文": "zh_CN",
        "🇮🇹 Italiano": "it_IT",
        "🇦🇪 اَلْعَرَبِيَّةُ": "ar_SA",
        "🇳🇱 Nederlands": "nl_NL",
        "🇧🇷 Português do Brasil": "pt_BR",
        "🇪🇸 español": "es_ES",
        "🇹🇷 Türkçe": "tr_TR",
        "🇮🇱 עברית": "he_IL",
        "🇷🇺 русский язык": "ru_RU",
        "🇫🇷 français": "fr_FR",
        "🇱🇰 සිංහල": "si_LK",
        "🇿🇦 Afrikaans": "af_ZA",
        "català": "ca_ES",
        "🇨🇿 čeština": "cs_CZ",
        "🇩🇰 dansk": "da_DK",
        "🇫🇮 suomen kieli": "fi_FI",
        "🇩🇪 Deutsch": "de_DE",
        "🇬🇷 ελληνικά": "el_GR",
        "🇭🇺 magyar nyelv": "hu_HU",
        "🇯🇵 日本語": "ja_JP",
        "🇰🇷 한국어": "ko_KR",
        "🇳🇴 norsk": "no_NO",
        "🇵🇱 polski": "pl_PL",
        "🇵🇹 português": "pt_PT",
        "🇷🇴 Daco-Romanian": "ro_RO",
        # "🇷🇸 српски језик": "sr_SP",
        "🇸🇪 svenska": "sv_SE",
        "🇺🇦 українська мова": "uk_UA",
        "🇻🇳 Tiếng Việt": "vi_VN",
        "🇮🇳 हिन्दी": "hi_IN",
        "🇮🇩 bahasa Indonesia": "id_ID",
        "🇺🇿 O'zbekcha": "uz_UZ",
        "🇲🇾 Bahasa Melayu": "ms_MY",
        "🇮🇳 தமிழ்": "ta_IN",
        "🇪🇹 አማርኛ": "am_ET",
        "🇰🇬 Кыргызча": "ky_KG",
    }
    LANGUAGE_SHORT_CODES = {x.split("_")[0]: x for x in LANGUAGE_CODES.values()}

    def __init__(self, language_repository: LanguageRepository) -> None:
        self.language_repository = language_repository

    def is_valid_language_value(self, value: str) -> bool:
        return value in self.LANGUAGE_CODES

    def get_language_code_from_short_code(self, short_code: str) -> str | None:
        return self.LANGUAGE_SHORT_CODES.get(short_code)

    async def send_language_options(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        query = update.callback_query
        if query is not None:
            await query.answer()

        user_lang = self.get_user_language(update, context)
        btns = [
            InlineKeyboardButton(key, callback_data=key)
            for key, value in sorted(self.LANGUAGE_CODES.items(), key=lambda x: x[1])
            if value != user_lang
        ]
        keyboard = [
            btns[i : i + self.LANGUAGES_KEYBOARD_SIZE]
            for i in range(0, len(btns), self.LANGUAGES_KEYBOARD_SIZE)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        _ = self.set_app_language(update, context)
        await update.effective_message.reply_text(  # type: ignore
            _("Select your language"), reply_markup=reply_markup
        )

    def get_user_language(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> str:
        if context.user_data is not None:
            lang: str | None = context.user_data.get(self.LANGUAGE)
            if lang is not None:
                return lang

        query: CallbackQuery | None = update.callback_query
        if query is None:
            sender = update.effective_message.from_user or update.effective_chat  # type: ignore
            user_id = sender.id  # type: ignore
        else:
            user_id = query.from_user.id

        lang = self.language_repository.get_language(user_id)
        if context.user_data is not None:
            context.user_data[self.LANGUAGE] = lang
        return lang

    async def update_user_language(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        query: CallbackQuery,
    ) -> None:
        await query.answer()
        lang_code = self.LANGUAGE_CODES.get(query.data)

        if lang_code is None:
            return

        self.language_repository.upsert_language(query.from_user.id, lang_code)
        context.user_data[self.LANGUAGE] = lang_code  # type: ignore
        _ = self.set_app_language(update, context)
        await query.message.edit_text(
            _("Your language has been set to {language}").format(language=query.data)
        )

    def set_app_language(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> Callable[[str], str]:
        lang = self.get_user_language(update, context)
        t = gettext.translation("pdf_bot", localedir="locale", languages=[lang])

        return t.gettext
