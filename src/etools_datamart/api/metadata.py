from rest_framework.metadata import SimpleMetadata


class SimpleMetadataWithFilters(SimpleMetadata):
    """Override SimpleMetadata, adding info about filters"""

    def determine_metadata(self, request, view):
        metadata = super(SimpleMetadataWithFilters, self).determine_metadata(request, view)
        metadata['filters'] = view.filter_fields
        metadata['filter_blacklist'] = view.filter_blacklist
        metadata['ordering'] = view.ordering_fields
        return metadata
