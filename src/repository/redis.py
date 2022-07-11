import json
from typing import List, Optional, Tuple

import orjson
from pydantic import BaseModel

from .base import ExpirationCache


class RedisCache(ExpirationCache):
    def put(self, key: str, entity: BaseModel) -> None:
        """
        Puts single entity model to cache with expiration timeout
        :param key: string consisting from parameters of query
        :param entity: entity model
        """
        self.cache_handler.set(
            key,
            orjson.dumps(entity.to_dict()),
            ex=self.expire,
        )

    def put_list(self, key: str, entities_list: List[BaseModel]) -> None:
        """
        Puts list of entities models to cache with expiration timeout
        :param key: string consisting from parameters of query
        :param entities_list: models list from cache
        """
        self.cache_handler.set(
            key,
            orjson.dumps([json.dumps(entity.to_dict()) for entity in entities_list]),
            ex=self.expire,
        )

    def exists(self, half_key: str) -> bool:
        return self._find_key(half_key) is not None

    def get(self, half_key: str):
        key = self._find_key(half_key)

        if not key:
            return None

        if "delete" in key or "create_all" in key:
            return self._get_list(key)

        return self._get(key)

    def _get(self, key: str) -> Tuple[dict, str]:
        """
        Return single entity from cache
        :param key: string consisting from parameters of query
        Returns:
            entity model if exists
        """

        _, operation = key.split("::")
        data = orjson.loads(self.cache_handler.get(key))
        self._delete(key)
        return data, operation

    def _get_list(self, key: str) -> Tuple[List[dict], str]:
        """
        Returns list of entities models from cache
        :param key: string consisting from parameters of query
        Returns:
            list on models
        """

        _, operation = key.split("::")
        data_raw = orjson.loads(self.cache_handler.get(key))
        data = [orjson.loads(event) for event in data_raw]
        self._delete(key)
        return data, operation

    def _delete(self, key) -> None:
        self.cache_handler.delete(key)

    def _find_key(self, key) -> Optional[str]:
        key = [key for key in self.cache_handler.scan_iter(f"{key}::*")]

        if not key:
            return None
        return key[0]

    def close(self):
        self.cache_handler.close()
