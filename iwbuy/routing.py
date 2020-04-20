from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing
from chat.routing import websocket_urlpatterns

# application = ProtocolTypeRouter({
#     "websocket": URLRouter(
#         websocket_urls,
#     ),
# })

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns,
        )
    ),
})