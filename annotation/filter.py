from django_filters import FilterSet

from .models import FunctionAnn


class FunctionFilter(FilterSet):
    class Meta:
        model = FunctionAnn
        fields = {
            "tr_id": ["contains"],
            'blast_hit': ["contains"],
            'description': ["contains"],
            'pfam': ["contains"],
            'interpro': ["contains"],
            'go': ["contains"],
        }
