import math
from django.test import TestCase

from ..models import Panel, PanelItem, Utestid
from ..utils import (
    load_panel_items_from_csv, load_utestids_from_csv, load_panels_from_csv
)


class TestGetresult(TestCase):

    def setUp(self):
        """Load testdata."""
        load_panels_from_csv()
        load_utestids_from_csv()
        load_panel_items_from_csv()

    def test_load(self):
        """Assert correct number of records created based on testdata."""
        self.assertEquals(Panel.objects.all().count(), 8)
        self.assertEquals(PanelItem.objects.all().count(), 6)
        self.assertEquals(Utestid.objects.all().count(), 6)

    def test_panel_item_string(self):
        """Asserts a string result is imported and formatted correctly."""
        panel = Panel.objects.create(name='Elisa')
        utestid = Utestid.objects.create(
            name='ELISA',
            value_type='absolute',
            value_datatype='string')
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid)
        value = panel_item.utestid.value('POS')
        self.assertEquals(value, 'POS')

    def test_panel_item_integer(self):
        """Asserts an integer result is imported and formatted correctly."""
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMH',
            value_type='absolute',
            value_datatype='integer',
        )
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid,
        )
        value = panel_item.utestid.value(100.99)
        self.assertEquals(value, 101)

    def test_panel_item_decimal(self):
        """Asserts a decimal result is imported and formatted correctly."""
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMH',
            value_type='absolute',
            value_datatype='decimal',
            precision=1)
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid)
        value = panel_item.utestid.value(100.77)
        self.assertEquals(value, 100.8)

    def test_panel_item_calc(self):
        """Asserts a calculated result is formatted correctly."""
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMHLOG',
            value_type='calculated',
            value_datatype='decimal',
            precision=2,
            formula='LOG10')
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid)
        value = panel_item.utestid.value(750000)
        self.assertEquals(value, round(math.log10(750000), 2))

    def test_panel_item_formula(self):
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMHLOG',
            value_type='calculated',
            value_datatype='decimal',
            precision=2,
            formula='1 + log10(100)')
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid,
        )
        self.assertRaises(ValueError, panel_item.utestid.value, 750000)

    def test_panel_item_quantifier_eq(self):
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMH',
            value_type='absolute',
            value_datatype='integer')
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid
        )
        value_with_quantifier = panel_item.utestid.value_with_quantifier(1000)
        self.assertEquals(value_with_quantifier, ('=', 1000))

    def test_panel_item_quantifier_lt(self):
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMH',
            value_type='absolute',
            value_datatype='integer',
            lower_limit=400,
            upper_limit=750000)
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid)
        value_with_quantifier = panel_item.utestid.value_with_quantifier(400)
        self.assertEquals(value_with_quantifier, ('=', 400))
        value_with_quantifier = panel_item.utestid.value_with_quantifier(399)
        self.assertEquals(value_with_quantifier, ('<', 400))

    def test_panel_item_quantifier_gt(self):
        panel = Panel.objects.create(name='viral load')
        utestid = Utestid.objects.create(
            name='PMH',
            value_type='absolute',
            value_datatype='integer',
            lower_limit=400,
            upper_limit=750000)
        panel_item = PanelItem.objects.create(
            panel=panel,
            utestid=utestid)
        value_with_quantifier = panel_item.utestid.value_with_quantifier(750000)
        self.assertEquals(value_with_quantifier, ('=', 750000))
        value_with_quantifier = panel_item.utestid.value_with_quantifier(750001)
        self.assertEquals(value_with_quantifier, ('>', 750000))
