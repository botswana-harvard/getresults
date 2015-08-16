import pytz
# from datetime import datetime

from django.conf import settings
from django.utils import timezone

from getresults_astm.records import Header, CommonPatient, OrderRecord, ResultRecord, TerminatorRecord

# from getresults_receive.models import Receive
from getresults_aliquot.models import Aliquot
from getresults_order.models import Order
from getresults_result.models import Result, ResultItem

from ..models import AstmQuery

from getresults.version import __version__


tz = pytz.timezone(settings.TIME_ZONE)


def emitter():

    def patient(patient_identifier, registration_datetime):
        return CommonPatient(
            practice_id=patient_identifier,
            admission_date=registration_datetime.strftime('%Y%m%d%H%M%S')
        )

    yield Header(
        sender=['getresults', __version__, '', ''],
    )

    for astm_query in AstmQuery.objects.filter(sent=False):
        try:
            aliquot = Aliquot.objects.get(aliquot_identifier=astm_query.aliquot_identifier)
            yield patient(aliquot.receive.receive_datetime)
            for order in Order.objects.filter(aliquot=aliquot):
                yield OrderRecord()
                for result in Result.objects.filter(order=order):
                    for _ in ResultItem.objects.filter(result=result):
                        yield ResultRecord()
        except Aliquot.DoesNotExist:
            yield patient(astm_query.patient_identifier, timezone.now())

    yield TerminatorRecord()
