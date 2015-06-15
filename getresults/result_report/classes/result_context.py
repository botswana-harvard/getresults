from ...models import Result, ResultItem


class ContextDescriptor(object):

    def __init__(self):
        self.value = {}

    def __get__(self, instance, owner):
        if instance.result_identifier:
            self.__set__(instance)
        return self.value

    def __set__(self, instance):
        self.value = {
            'last_updated': instance.result.modified,
            'result': instance.result,
            'protocol_identifier': instance.result.order.aliquot.receive.protocol.protocol_identifier,
            'subject_identifier': instance.result.order.aliquot.receive.patient.subject_identifier,
            'dob': instance.result.order.aliquot.receive.patient.dob,
            'is_dob_estimated': instance.result.order.aliquot.receive.patient.is_dob_estimated,
            'gender': instance.result.order.aliquot.receive.patient.gender,
            'initials': instance.result.order.aliquot.receive.patient.initials,
            'site_identifier': instance.result.order.aliquot.receive.site.site_identifier,
            'clinicians_initials': instance.result.order.get_requisition('clinicians_initials'),
            'drawn_datetime': instance.result.order.aliquot.receive.drawn_datetime,
            'panel_name': instance.result.order.panel.name,
            'receive_identifier': instance.result.order.aliquot.receive.receive_identifier,
            'receive_datetime': instance.result.order.aliquot.receive.receive_datetime,
            'aliquot_identifier': instance.result.order.aliquot.aliquot_identifier,
            'order_identifier': instance.result.order.order_identifier,
            'order_datetime': instance.result.order.order_datetime,
            'condition': instance.result.order.aliquot.aliquot_condition,
            #'receive': result.order.getresults_aliquot.receive,
            #'order': result.order,
            #'getresults_aliquot': result.order.getresults_aliquot,
            'result_items': instance.result_items,
            'action': "view",
            'section_name': instance.section_name,
            'search_name': instance.search_name,
            'result_include_file': "detail.html",
            'receiving_include_file': "receiving.html",
            'orders_include_file': "orders.html",
            'result_items_include_file': "result_items.html",
            'top_result_include_file': "result_include.html",
            }


class ResultContext(object):

    context = ContextDescriptor()

    def __init__(self, **kwargs):
        self.section_name = kwargs.get('section_name')
        self.search_name = kwargs.get('search_name')
        self.result_identifier = kwargs.get('result_identifier')
        if self.result_identifier:
            self.result = Result.objects.get(result_identifier__exact=self.result_identifier)
            self.result_items = ResultItem.objects.filter(result=self.result)
            #self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.result.lab.subject_identifier)        

