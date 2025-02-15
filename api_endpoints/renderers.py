from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = data

        # Ensure errors are not unnecessarily wrapped
        if isinstance(data, dict) and "errors" in data:
            response = json.dumps(data)  # Keep the original format
        else:
            response = json.dumps(data)

        return response
