from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import os.path

from notebook.base.handlers import FileFindHandler
from tornado.web import HTTPError

_static_dir = os.path.join(os.path.dirname(__file__), 'static')

class HelloWorldHandler(IPythonHandler):
    def get(self):
        self.finish('Hello, world!')

class StaticFilesHandler(FileFindHandler):
    @classmethod
    def get_absolute_path(cls, base_path, requested_file):
        """locate a file to serve on our static file search path"""
        print("base_path: %s, requested_file: %s" % (base_path, requested_file))
        assert len(base_path) == 1
        base_path = base_path[0]
        print('joined ', os.path.join(base_path, requested_file))
        target_file = os.path.realpath(os.path.abspath(os.path.join(base_path, requested_file)))
        print('target_file ', target_file)

        if not target_file.startswith(base_path):
            print(base_path)
            print(target_file)
            raise HTTPError(403, "access to %s is not allowed", target_file)

        if not os.path.isfile(target_file):
            raise HTTPError(404, "%s is not in the static directory", target_file)

        return target_file

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/jade_ex/static/(.*)')
    web_app.add_handlers(host_pattern, [(route_pattern, StaticFilesHandler, {'path': _static_dir})])
