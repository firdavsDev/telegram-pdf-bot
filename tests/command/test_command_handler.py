from unittest.mock import MagicMock

import pytest
from telegram.ext import CommandHandler as TelegramCommandHandler
from telegram.ext import filters

from pdf_bot.command import CommandHandler, CommandService
from tests.telegram_internal import TelegramTestMixin


class TestLanguageHandler(TelegramTestMixin):
    START_COMMAND = "start"
    HELP_COMMAND = "help"
    SEND_COMMAND = "send"
    ADMIN_TELEGRAM_ID = 123

    def setup_method(self) -> None:
        super().setup_method()
        self.command_service = MagicMock(spec=CommandService)
        self.sut = CommandHandler(self.command_service, self.ADMIN_TELEGRAM_ID)

    @pytest.mark.asyncio
    async def test_handlers(self) -> None:
        actual = self.sut.handlers
        assert len(actual) == 3

        handler_0 = actual[0]
        assert isinstance(handler_0, TelegramCommandHandler)
        assert handler_0.commands == {self.START_COMMAND}

        handler_1 = actual[1]
        assert isinstance(handler_1, TelegramCommandHandler)
        assert handler_1.commands == {self.HELP_COMMAND}

        handler_2 = actual[2]
        assert isinstance(handler_2, TelegramCommandHandler)
        assert handler_2.commands == {self.SEND_COMMAND}
        assert handler_2.filters.name == filters.User(self.ADMIN_TELEGRAM_ID).name

        for handler in actual:
            await handler.callback(self.telegram_update, self.telegram_context)

        self.command_service.send_start_message.assert_called_once()
        self.command_service.send_help_message.assert_called_once()
        self.command_service.send_message_to_user.assert_called_once()