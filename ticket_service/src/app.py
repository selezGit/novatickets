from flask import Flask, render_template, request
from flask.views import MethodView

from core.config import CONSUMER_HOST, MSG_TEMPLATE, DEBUG
from db.redis import redis_handler
from repository.redis import RedisCache
from services.event import EventService
from services.exceptions import EventSpecifiedTimeAlreadyCreated, IntersectionEventsError

app = Flask(__name__)


class ConfirmView(MethodView):
    _cache = RedisCache(redis_handler)
    _event = EventService()

    def get(self):
        args = request.args
        key = args.get("key")

        context = {
            "title": "Error",
            "message": "Ссылка уже активирована либо срок действия ссылки истёк",
        }
        if key and self._cache.exists(key):
            data, operation = self._cache.get(key)

            try:
                self._event.do_task(operation, data)
                context["title"] = f"Success"
                context["message"] = MSG_TEMPLATE[operation]

            except (
                IntersectionEventsError,
                EventSpecifiedTimeAlreadyCreated,
            ) as error:
                context["message"] = error

        return render_template("base.html", context=context)


app.add_url_rule("/confirm", view_func=ConfirmView.as_view("confirm"))


if __name__ == "__main__":
    app.run(host=CONSUMER_HOST, debug=DEBUG)
