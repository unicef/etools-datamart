import io
import os

from django.conf import settings
from django.template import loader
from xhtml2pdf import pisa

from .html import HTMLRenderer


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL  # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL  # Typically /static/media/
    mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path


class PDFRenderer(HTMLRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    charset = 'utf-8'
    render_style = 'text'

    def get_template(self, meta):
        return loader.select_template([
            f'renderers/pdf/{meta.app_label}/{meta.model_name}.html',
            'renderers/pdf/pdf.html'])

    def render(self, data, accepted_media_type=None, renderer_context=None):
        html = super(PDFRenderer, self).render(data, accepted_media_type, renderer_context)
        # create a pdf
        buffer = io.BytesIO()
        pisaStatus = pisa.CreatePDF(html, dest=buffer, link_callback=link_callback)
        # if error then show some funy view
        if pisaStatus.err:
            raise Exception('We had some errors <pre>' + html + '</pre>')
        buffer.seek(0)
        return buffer.read()
