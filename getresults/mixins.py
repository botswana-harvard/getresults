import pytz

from uuid import uuid4
from django.conf import settings
from getresults_aliquot.models import Aliquot, AliquotType, AliquotCondition
from getresults_order.models import (
    OrderPanel, OrderPanelItem, Order, Utestid)
from getresults_sender.models import Sender, SenderPanel, SenderPanelItem
from getresults_receive.models import Receive
from getresults_result.models import Result, ResultItem

tz = pytz.timezone(settings.TIME_ZONE)


class GetresultsDbMixin(object):

    def sender(self, sender_name, sender_description):
        """Gets and returns a sender record.

        Creates a sender record if it does not exist."""
        try:
            sender = Sender.objects.get(name=sender_name)
        except Sender.DoesNotExist:
            sender = Sender.objects.create(
                name=sender_name,
                description=sender_description)
        return sender

    def order_panel(self, name):
        """Gets and returns a Panel record.

        Creates a Panel record if create_dummy_records = True."""
        try:
            order_panel = OrderPanel.objects.get(name=name)
        except OrderPanel.DoesNotExist:
            order_panel = OrderPanel.objects.create(name=name)
        return order_panel

    def order(self, order_identifier, order_datetime, action_code, report_type, order_panel, receive):
        """Gets and returns a Order record.

        Creates a Order record if create_dummy_records = True."""
        try:
            order = Order.objects.get(order_identifier=order_identifier)
        except Order.DoesNotExist:
            order = None
            if self.create_dummy_records:
                aliquot = self.aliquot(receive, order_identifier)
                order = Order.objects.create(
                    order_identifier=order_identifier,
                    order_datetime=tz.localize(order_datetime),
                    # specimen_identifier=order_identifier,
                    # action_code=action_code,
                    # report_type=report_type,
                    order_panel=order_panel,
                    aliquot=aliquot)
        return order

    def aliquot(self, receive, order_identifier):
        """Gets and returns an aliquot record.

        Will create a primary if create_dummy_records is True."""
        try:
            aliquot_type = AliquotType.objects.get(name='unknown')
        except AliquotType.DoesNotExist:
            aliquot_type = AliquotType.objects.create(name='unknown', numeric_code='00', alpha_code='00')
        try:
            AliquotCondition.objects.get(name='unknown')
        except AliquotCondition.DoesNotExist:
            AliquotCondition.objects.create(name='unknown', description='unknown')
        try:
            aliquot = Order.objects.get(
                order_identifier=order_identifier
            ).aliquot
        except Order.DoesNotExist:
            aliquot = None
            if self.create_dummy_records:
                aliquot = Aliquot.objects.create_primary(receive, aliquot_type.numeric_code)
        return aliquot

    def receive(self, patient, receive_identifier, collection_datetime, receive_datetime, batch_id=None):
        """Gets and returns a Receive record.

        Creates a Receive record if create_dummy_records = True."""
        try:
            receive = Receive.objects.get(
                receive_identifier=receive_identifier,
            )
        except Receive.DoesNotExist:
            receive = None
            if self.create_dummy_records:
                receive = Receive.objects.create(
                    receive_identifier=receive_identifier,
                    collection_datetime=collection_datetime,
                    receive_datetime=receive_datetime,
                    patient=patient,
                    batch_id=batch_id or uuid4(),
                )
        return receive

    def result(self, result_identifier, order, specimen_identifier, operator, status, instrument):
        """Gets and returns a Result record.

        Creates a Result record if create_dummy_records = True."""
        try:
            result = Result.objects.get(order=order)
        except Result.DoesNotExist:
            result = Result.objects.create(
                order=order,
                result_identifier=result_identifier,
                specimen_identifier=specimen_identifier,
                status=status,
                operator=operator,
                analyzer_name=instrument
            )
        return result

    def sender_panel(self, name):
        """Gets and returns a Panel record.

        Creates a Panel record if create_dummy_records = True."""
        try:
            sender_panel = SenderPanel.objects.get(name=name)
        except SenderPanel.DoesNotExist:
            sender_panel = SenderPanel.objects.create(name=name)
        return sender_panel

    def utestid(self, name):
        try:
            utestid = Utestid.objects.get(name=name)
        except Utestid.DoesNotExist:
            utestid = Utestid.objects.create(
                name=name,
                value_type='absolute',
                value_datatype='string',
                description='unknown from interface')
        return utestid

    def order_panel_item(self, panel, utestid):
        try:
            order_panel_item = OrderPanelItem.objects.get(
                panel=panel,
                utestid=utestid
            )
        except OrderPanelItem.DoesNotExist:
            order_panel_item = OrderPanelItem.objects.create(
                panel=panel,
                utestid=utestid
            )
        return order_panel_item

    def sender_panel_item(self, panel, utestid):
        try:
            sender_panel_item = SenderPanelItem.objects.get(
                panel=panel,
                utestid=utestid
            )
        except SenderPanelItem.DoesNotExist:
            sender_panel_item = SenderPanelItem.objects.create(
                panel=panel,
                utestid=utestid
            )
        return sender_panel_item

    def result_item(self, result, utestid, result_record):
        try:
            result_item = ResultItem.objects.get(
                result=result,
                utestid=utestid)
        except ResultItem.DoesNotExist:
            result_item = ResultItem()
        result_item.result = result
        result_item.utestid = utestid
        result_item.specimen_identifier = result.specimen_identifier
        result_item.status = result_record.status
        result_item.operator = result_record.operator
        if result_record.value[0] in '=<>':
            result_item.quantifier, result_item.value = result_record.value[0], result_record.value[1:]
        else:
            result_item.quantifier, result_item.value = utestid.value_with_quantifier(result_record.value)
        result_item.raw_value = result_record.value
        try:
            result_item.result_datetime = tz.localize(result_record.completed_at)
        except ValueError as e:
            if 'Not naive datetime' in str(e):
                result_item.result_datetime = result_record.completed_at
            else:
                raise
        result_item.save()
        return result_item
