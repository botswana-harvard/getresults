
# load orders
# load senders
# load csv

from getresults_csv.configure import Configure as ConfigureCsv
from getresults_order.configure import Configure as ConfigureOrder
from getresults_sender.configure import Configure as ConfigureSender


class Configure(object):

    def load_all(self):
        configure_order = ConfigureOrder()
        configure_order.load_all()
        configure_sender = ConfigureSender()
        configure_sender.load_all()
        configure_csv = ConfigureCsv()
        configure_csv.load_all()
