from redis import Redis

from django.conf import settings


class RedisClient:
    """
    Обертка для редис-клиента
    """

    def __init__(self, host: str, port: int, decode=True):
        self.r = Redis(host=host, port=port, decode_responses=decode)

    @staticmethod
    def from_settings():
        channel_redis_sett = (
            settings.CHANNEL_LAYERS.get("default").get("CONFIG").get("hosts")
        )
        decode = True
        if not channel_redis_sett:
            channel_redis_sett = [("localhost", 6379)]
        return RedisClient(
            channel_redis_sett[0][0], channel_redis_sett[0][1], decode
        )

    @staticmethod
    def from_credentials(host, port, decode=True):
        return RedisClient(host, port, decode)

    def debug_print_key(self, key):
        print(self.r.get(key))

    def get_message(self, chat: str, hashcode: str):
        return self.r.hgetall(chat + ":" + hashcode)

    def get_message_by_key(self, key: str):
        return self.r.hgetall(key)

    def store_message(self, chat: str, hashcode: str, message: dict):
        print("В обертке редиска мессага:")
        print(message)
        self.r.hset(
            chat + ":" + hashcode,
            mapping=message,
        )

    def store_multiple_messages(self, chat: str, messages: dict):
        for key, value in messages.items():
            self.store_message(chat, key, value)

    def delete(self, hashcodes):
        for code in hashcodes:
            self.r.delete(code)

    def search_by_pattern(self, pattern: str):
        result = []
        for name in self.r.scan_iter(match=pattern):
            result.append(name)
        return result
