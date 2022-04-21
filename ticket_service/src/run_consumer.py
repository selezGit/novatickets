from flask import Flask, jsonify, request
from flask.views import MethodView

from db.redis import redis_handler
from repository.redis import RedisCache
from services.event import EventService
from core.config import CONSUMER_HOST
app = Flask(__name__)


class ConfirmView(MethodView):
    _cache = RedisCache(redis_handler)
    _event = EventService()

    def get(self):
        args = request.args
        key = args.get("key")
        if key and self._cache.exists(key):
            data, operation = self._cache.get(key)
            if self._event.do_task(operation, data):
                return jsonify(status="success")
                
        return jsonify(status="error")


app.add_url_rule("/confirm", view_func=ConfirmView.as_view("confirm"))


if __name__ == "__main__":
    app.run(host=CONSUMER_HOST, debug=True)
