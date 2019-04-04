from rest_framework.permissions import AllowAny
from rest_framework_swagger import renderers
from rest_framework.schemas import get_schema_view


schema_view = get_schema_view(title="Hasker API", public=True,
                              renderer_classes=[renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer],
                              permission_classes=[AllowAny])
