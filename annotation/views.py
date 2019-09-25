from django.shortcuts import render
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin
from django_tables2.export.views import ExportMixin
from .models import FunctionAnn
from .tables import FuncTable
from .filter import FunctionFilter

#class FunctionAnnView(SingleTableView):
#    model = FunctionAnn
#    table_class = FuncTable
#    template_name = 'annotation/function.html'


class FunctionAnnView(ExportMixin, SingleTableMixin, FilterView):
    table_class = FuncTable
    model = FunctionAnn
    template_name = "annotation/function.html"

    filterset_class = FunctionFilter

    export_formats = ("csv", "xls")

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}
