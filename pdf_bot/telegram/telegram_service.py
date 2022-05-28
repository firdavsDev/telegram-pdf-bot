from contextlib import contextmanager
from typing import Generator, List

from telegram import Bot
from telegram.ext import Updater

from pdf_bot.io import IOService


class TelegramService:
    def __init__(
        self,
        io_service: IOService,
        updater: Updater | None = None,
        bot: Bot | None = None,
    ) -> None:
        self.io_service = io_service
        self.bot = bot or updater.bot

    @contextmanager
    def download_file(self, file_id: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_file() as out_path:
            try:
                file = self.bot.get_file(file_id)
                file.download(custom_path=out_path)
                yield out_path
            finally:
                pass

    @contextmanager
    def download_files(self, file_ids: List[str]) -> Generator[List[str], None, None]:
        with self.io_service.create_temp_files(len(file_ids)) as out_paths:
            try:
                for i, file_id in enumerate(file_ids):
                    file = self.bot.get_file(file_id)
                    file.download(custom_path=out_paths[i])
                yield out_paths
            finally:
                pass