import abc
from typing import List, Optional, Union

import orjson
from pydantic import BaseModel

from core.config import CACHE_EXPIRE_IN_SECONDS


class BaseModelCache:

    cache_key_separator = "::"

    def __init__(self, cache_handler):
        self.cache_handler = cache_handler
        self.model = None

    @abc.abstractmethod
    async def put(self, entity: BaseModel) -> None:
        pass

    @abc.abstractmethod
    async def put_list(self, key: str, entities_list: List[BaseModel]):
        pass

    @abc.abstractmethod
    async def get(self, entity_id: str) -> Optional[BaseModel]:
        pass

    @abc.abstractmethod
    async def get_list(self, key: str) -> Optional[List[BaseModel]]:
        pass

    @abc.abstractmethod
    def close(self):
        pass

    def get_cache_key(self, prefix: str = "", **kwargs) -> str:
        """
        Returns key for cache consisting from prefix of index name and args values
        :param prefix:
        :param kwargs: function call params identifying func result
        Returns:
            cache key
        """
        memo = []
        for arg, value in sorted(kwargs.items()):
            if isinstance(value, dict):
                memo.extend([self.get_memo_item(key, key_value) for key, key_value in sorted(value.items())])
            else:
                memo.append(self.get_memo_item(arg, value))
        return prefix + self.cache_key_separator + self.cache_key_separator.join(memo)

    def get_memo_item(self, key: str, value: Union[str, int, float]) -> str:
        """
        Returns part of cache key consisting from given arg name and its value casted to str with separator
        :param key: arg name
        :param value: arg value castable to str
        Returns:
            part of cache key
        """
        return key + self.cache_key_separator + str(value)

    def set_model(self, model: BaseModel) -> None:
        self.model = model


class RedisCache(BaseModelCache):
    async def put(self, entity: BaseModel, expire: int):
        """
        Puts single entity model to cache with expiration timeout
        :param entity: entity model
        """
        key = getattr(entity, "key", None)

        if key is None:
            raise ValueError("Use model with `key` field")
        await self.cache_handler.set(
            key,
            entity.json(),
            expire=expire,
        )

    async def put_list(self, key: str, entities_list: List[BaseModel]):
        """
        Puts list of entities models to cache with expiration timeout
        :param key: string consisting from parameters of query
        :param entities_list: models list from cache
        """
        await self.cache_handler.set(
            key,
            orjson.dumps([entity.json() for entity in entities_list]),
        )

    async def get(self, entity_id: str) -> Optional[BaseModel]:
        """
        Return single entity from cache
        :param: entity_id: uuid of entity
        Returns:
            entity model if exists
        """
        data = await self.cache_handler.get(entity_id)
        if not data:
            return None
        entity = self.model.parse_raw(data)
        return entity

    async def get_list(self, key: str) -> Optional[List[BaseModel]]:
        """
        Returns list of entities models from cache
        :param key: string consisting from parameters of query
        Returns:
            list on models
        """
        data_raw = await self.cache_handler.get(key)
        if not data_raw:
            return None
        data = orjson.loads(data_raw)
        result = [self.model.parse_raw(entity) for entity in data]
        return result

    async def close(self):
        await self.cache_handler.close()
