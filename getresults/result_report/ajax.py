from django.template.loader import render_to_string
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from lis.specimen.lab_result.models import Result
from lis.specimen.lab_result_item.models import ResultItem


@dajaxice_register
def print_result_report(request, result_identifier):
    dajax = Dajax()
    if result_identifier is not None:
        result = Result.objects.using('lab_api').get(result_identifier__exact=result_identifier)
        result_items = ResultItem.objects.using('lab_api').filter(result=result)
        context = {
        'result': result,
        'receive': result.order.aliquot.receive,
        'order': result.order,
        'getresults_aliquot': result.order.aliquot,
        'result_items': result_items,
        'result_include_file': "detail.html",
        'receiving_include_file': "receiving.html",
        'orders_include_file': "orders.html",
        'result_items_include_file': "result_items.html",
        'top_result_include_file': "result_include.html",
        }
    rendered = render_to_string('result_report_single.html', {'result_report': context})
    dajax.assign('#result_report', 'innerHTML', rendered)
    return dajax.json()
