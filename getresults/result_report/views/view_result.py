from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from ...models import Result
from ..classes import ResultContext


@login_required
def view_result(request, **kwargs):

    result_identifier = kwargs.get('result_identifier')
    template = 'result_report.html'
    if result_identifier is not None:
        result_context = ResultContext(result_identifier=result_identifier)
        return render_to_response(
            template,
            result_context.context,
            context_instance=RequestContext(request)
        )


def render_search(**kwargs):
    return Result.objects.filter(result_identifier=kwargs['search_term'])
