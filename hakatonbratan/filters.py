from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        admin_ids = {1427364974}
        if message.from_user.id in admin_ids:
            return True
        else:
            return False