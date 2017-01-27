from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os.path

from notebook.base.handlers import FileFindHandler

_static_dir = os.path.join(os.path.dirname(__file__), 'static')

class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish('Hello, world!')

class FilesHandler(FileFindHandler):
    pass
    # @staticmethod
    # def get_absolute_path(path):
    #     print(path)

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/jade_ex/static/(.*)')
    web_app.add_handlers(host_pattern, [(route_pattern, FileFindHandler, {'path': _static_dir})])
