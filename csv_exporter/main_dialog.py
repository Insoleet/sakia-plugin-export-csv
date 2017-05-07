from sakia.data.processors.connections import ConnectionsProcessor
from sakia.data.entities import Transaction
from .csv_exporter_uic import Ui_CSVExporter
from PyQt5.QtWidgets import QDialog, QFileDialog
import csv


class MainDialog(QDialog, Ui_CSVExporter):
    def __init__(self, app, main_window):
        """
        
        :param sakia.app.Application app: 
        :param main_window: 
        """
        super().__init__(main_window.view)

        self.setupUi(self)
        self.button_export.clicked.connect(self.export_csv)
        self.connections_processor = ConnectionsProcessor.instanciate(app)
        for conn in self.connections_processor.connections():
            self.combo_connections.addItem(conn.title())
        self.app = app

    def export_csv(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export to...", None,
                                    "CSV-File (*.csv);;All Files (*)")

        if filename:
            if not filename.endswith(".csv"):
                filename += ".csv"

            connection_text = self.combo_connections.currentText()
            connection = None
            for conn in self.connections_processor.connections():
                if conn.title() == connection_text:
                    connection = conn

            transfers = self.app.transactions_service.transfers(connection.pubkey)
            dividends = self.app.transactions_service.dividends(connection.pubkey)
            sorted_data = [] + transfers + dividends
            sorted_data.sort(key=lambda x: x.timestamp)
            with open(filename, 'w', newline='') as csvfile:
                field_names = ['timestamp', 'from/to', 'amount']
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                for data in sorted_data:
                    if isinstance(data, Transaction):
                        amount = data.amount * 10**data.amount_base
                        if connection.pubkey in data.issuers:
                            from_to = "\n".join(data.receivers)
                            amount *= -1
                        else:
                            from_to = "\n".join(data.issuers)
                    else:
                        from_to = connection.pubkey
                        amount = data.amount * 10 ** data.base
                    writer.writerow({'timestamp': data.timestamp,
                                     'from/to': from_to,
                                     'amount': str(amount/100).replace(".", ",")})


