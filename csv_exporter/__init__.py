PLUGIN_NAME = "CSV Exporter plugin"
PLUGIN_DESCRIPTION = "A plugin to export csv from transactions history"
PLUGIN_VERSION = "0.1"

from .main_dialog import MainDialog


def plugin_exec(app, main_window):
    """
    :param sakia.app.Application app:
    :param sakia.gui.main_window.controller.MainWindowController main_window:
    """
    from PyQt5.QtWidgets import QAction
    tool_menu = main_window.toolbar.view.toolbutton_menu.menu()
    action_open_example = QAction("CSV Exporter", tool_menu)
    tool_menu.addAction(action_open_example)
    action_open_example.triggered.connect(lambda c, a=app, mw=main_window: open_dialog(a, mw))


def open_dialog(app, main_window):
    """
    :param sakia.app.Application app:
    :param sakia.gui.main_window.controller.MainWindowController main_window:
    """
    dialog = MainDialog(app, main_window)
    dialog.exec()

