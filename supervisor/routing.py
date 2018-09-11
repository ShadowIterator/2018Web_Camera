# supervisor/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import videoprocess.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            videoprocess.routing.websocket_urlpatterns
        )
    ),
})

# mysite/routing.py
# from channels.routing import ProtocolTypeRouter
#
# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
# })