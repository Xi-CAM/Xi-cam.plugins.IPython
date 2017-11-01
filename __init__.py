import sys

# Hack to work around PySide being imported from nowhere:
import qtpy

from xicam.plugins import IGUIPlugin, GUILayout

# Overload for Py2App
# def new_load_qt(api_options):
#     from qtpy import QtCore, QtWidgets, QtSvg
#
#     return QtCore, QtWidgets, QtGuiCompat, 'pyqt5'
# from qtconsole import qt_loaders
# qt_loaders.load_qt(['pyqt5'])
if 'PySide.QtCore' in sys.modules and qtpy.API != 'pyside': del sys.modules['PySide.QtCore']

from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.inprocess import QtInProcessKernelManager


class IPythonPlugin(IGUIPlugin):
    name = 'IPython'

    def __init__(self):
        # with open('xicam/gui/style.stylesheet', 'r') as f:
        #     style = f.read()
        # style = (qdarkstyle.load_stylesheet() + style)

        kernel_manager = QtInProcessKernelManager()
        kernel_manager.start_kernel()
        kernel = kernel_manager.kernel
        kernel.gui = 'qt'
        # kernel.shell.push(dict(plugins.plugins))

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        def stop():
            kernel_client.stop_channels()
            kernel_manager.shutdown_kernel()

        control = RichJupyterWidget()
        control.kernel_manager = kernel_manager
        control.kernel_client = kernel_client
        control.exit_requested.connect(stop)
        # control.style_sheet = style
        control.syntax_style = u'monokai'
        control.set_default_style(colors='Linux')

        self.centerwidget = control

        self.stages = {'Terminal': GUILayout(control)}

        super(IPythonPlugin, self).__init__()
