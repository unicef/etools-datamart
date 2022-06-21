from django.utils.encoding import smart_str

from rest_framework_xml.renderers import XMLRenderer


class MSXmlRenderer(XMLRenderer):
    media_type = 'application/xml'
    format = 'ms-xml'
    root_tag_name = "DocumentElement"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        view = renderer_context['view']
        self.item_tag_name = view.get_queryset().model._meta.model_name
        return super().render(data, accepted_media_type, renderer_context)

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement(self.item_tag_name, {})
                self._to_xml(xml, item)
                xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in data.items():
                xml.startElement(key.upper(), {})
                self._to_xml(xml, value)
                xml.endElement(key.upper())

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(smart_str(data))
