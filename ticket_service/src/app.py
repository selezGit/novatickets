from flask import Flask, request, render_template
from flask.views import MethodView

from db.redis import redis_handler
from repository.redis import RedisCache
from services.event import EventService
from core.config import CONSUMER_HOST, MSG_TEMPLATE


app = Flask(__name__)


class ConfirmView(MethodView):
    _cache = RedisCache(redis_handler)
    _event = EventService()

    def get(self):

        args = request.args
        key = args.get("key")

        context = {}
        if key and self._cache.exists(key):
            data, operation = self._cache.get(key)
            if self._event.do_task(operation, data):

                context["title"] = f"Success"
                context["message"] = MSG_TEMPLATE[operation]
                return render_template("base.html", context=context)

        context["title"] = f"Error"
        context["message"] = f"Ссылка уже активирована либо срок действия ссылки истёк"
        return render_template("base.html", context=context)


app.add_url_rule("/confirm", view_func=ConfirmView.as_view("confirm"))


if __name__ == "__main__":
    app.run(host=CONSUMER_HOST, debug=True)