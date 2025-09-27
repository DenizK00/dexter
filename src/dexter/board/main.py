import sys
import subprocess
import threading
from PyQt5 import QtWidgets, QtCore
from ipykernel.kernelapp import IPKernelApp
from IPython import get_ipython
import dash
from dash import dcc, html, Input, Output, dash_table
from dash.dependencies import State
import dash_bootstrap_components as dbc
import pandas as pd
import jp_proxy_widget

class IPKernel:
    def __init__(self):
        self.kernel_app = None
        self.kernel_thread = None
        self.exposed_instance = None  # To store the instance to be accessed from IPython

    def start(self):
        if self.kernel_thread is None or not self.kernel_thread.is_alive():
            self.kernel_thread = threading.Thread(target=self._start_kernel, daemon=True)
            self.kernel_thread.start()

    def _start_kernel(self):
        try:
            self.kernel_app = IPKernelApp.instance()
            if not self.kernel_app.initialized:
                self.kernel_app.initialize(['python'])
                self.kernel_app.start()
        except Exception as e:
            print(f"Kernel initialization failed: {e}")
            # Don't re-raise the exception to prevent import failures

    def new_qt_console(self):
        connection_file = self.kernel_app.connection_file
        config_file_path = 'console_config.py'  # Relative path to the config file
        process = subprocess.Popen([
            'jupyter', 'qtconsole', '--existing', connection_file,
            '--config', config_file_path
        ])
        return process

    def print_namespace(self):
        ipython = get_ipython()
        if ipython:
            print(ipython.user_ns)
        else:
            print("No IPython kernel running.")

    def count(self):
        ipython = get_ipython()
        if ipython:
            if 'counter' not in ipython.user_ns:
                ipython.user_ns['counter'] = 0
            ipython.user_ns['counter'] += 1
            print(f"Counter: {ipython.user_ns['counter']}")
        else:
            print("No IPython kernel running.")

    def inject(self, instance, name: str = None):
        """Expose an instance to the IPython kernel namespace."""
        ipython = get_ipython()
        if not name:
            name = str(instance)

        if ipython:
            ipython.push({name: instance})
        else:
            print("No IPython kernel running.")

    def cleanup_consoles(self):
        print("Cleaning up consoles")
    
    def is_running(self):
        """Check if the kernel is running."""
        return (self.kernel_app is not None and 
                hasattr(self.kernel_app, 'initialized') and 
                self.kernel_app.initialized)

# Initialize the custom IPython kernel (but don't start it automatically)
main_kernel = IPKernel()
# Note: Kernel will be started when needed, not on import

# Sample DataFrame
df = pd.DataFrame({
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": ["p", "q", "r"]
})

# Setup the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Initialize a Jupyter proxy widget for the IPython terminal
# jupyter_widget = jp_proxy_widget.JupyterProxyWidget()
# jupyter_widget.load_jupyter_extension()

def get_jupyter_widget_html():
    """Function to integrate Jupyter widget in Dash."""
    # Note: jupyter_widget is commented out above, so this function is not currently used
    # return jupyter_widget.element.html()
    return "Jupyter widget HTML would go here"

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Viewer"),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'height': '300px', 'overflowY': 'auto'}
            )
        ], width=6),
        dbc.Col([
            html.H1("IPython Terminal"),
            html.Div(id='jupyter-terminal', children=[])
            # Using Custom Kernel instead?
        ], width=6)
    ])
])

# Callbacks to handle interactions (add as needed)

if __name__ == '__main__':
    app.run_server(debug=True)
