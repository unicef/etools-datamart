from rest_framework_xml.renderers import XMLRenderer


class MSXmlRenderer(XMLRenderer):
    media_type = 'application/xml'
    format = 'ms-xml'
