class ContentDispositionMixin:
    def process_response(self, renderer_context):
        response = renderer_context["response"]
        view = renderer_context["view"]
        try:
            filename = view.get_service().basename
        except Exception:
            filename = self.__class__.__name__
        response["Content-Disposition"] = 'attachment; filename="%s.%s"' % (filename, self.format)
        return response
