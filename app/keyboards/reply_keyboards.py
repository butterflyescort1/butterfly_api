from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from urllib.parse import urlparse, ParseResult

from data.config import buttons


class StartKeyboard:
    def __init__(self, url: str, user_id: int):
        self.url = url
        if self.url.endswith("/"):
            self.url = self.url[:-1]
        self.user_id = user_id
    
    def get_start_keyboard(self) -> ReplyKeyboardMarkup:        
        builder = ReplyKeyboardBuilder()

        builder.add(KeyboardButton(
            text=buttons["aboutButton"],
            web_app=self._get_web_app_info("about")
        ))
        builder.add(KeyboardButton(
            text=buttons["guaranteesButton"],
            web_app=self._get_web_app_info("guarantees")
        ))
        builder.add(KeyboardButton(
            text=buttons["butterflyButton"],
            web_app=self._get_web_app_info("butterfly")
        ))
        builder.add(KeyboardButton(
            text=buttons["ordersButton"],
            web_app=self._get_web_app_info("orders")
        ))
        builder.add(KeyboardButton(
            text=buttons["supportButton"],
            web_app=self._get_web_app_info("support")
        ))
        
        builder.adjust(2, 1)
        return builder.as_markup(resize_keyboard=True)
    
    def _get_web_app_info(self, endpoint: str) -> WebAppInfo:
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]
        
        url_parsed = urlparse(self.url)
        url_parsed = ParseResult(
            scheme=url_parsed.scheme,
            netloc=url_parsed.netloc,
            path=endpoint,
            params=url_parsed.params,
            query=f"tg_id={self.user_id}",
            fragment=url_parsed.fragment
        )
        return WebAppInfo(url=url_parsed.geturl())
