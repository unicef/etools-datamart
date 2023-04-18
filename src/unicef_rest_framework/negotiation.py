from rest_framework.negotiation import DefaultContentNegotiation


class CT(DefaultContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix=None):
        format_query_param = self.settings.URL_FORMAT_OVERRIDE
        format = format_suffix or request.query_params.get(format_query_param)
        if format == "iqy":
            for renderer in renderers:
                if renderer.format == format:
                    return renderer, renderer.media_type

        return super().select_renderer(request, renderers, format_suffix)
