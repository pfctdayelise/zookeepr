"""Pylons environment configuration"""
import os

from mako.lookup import TemplateLookup
#from zookeepr.lib.template import ZookeeprTemplateLookup as TemplateLookup
from pylons import config
from pylons.error import handle_mako_error
from sqlalchemy import engine_from_config

import zookeepr.lib.app_globals as app_globals
import zookeepr.lib.helpers
from zookeepr.config.routing import make_map
from zookeepr.model import init_model

from zookeepr.config.lca_info import lca_info
from zookeepr.config.zookeepr_config import file_paths

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=[file_paths['theme_public'], file_paths['public_path']],
                 templates=[os.path.join(root, 'templates')],           # apparently pylons still wants this and as a list
                 default_theme=file_paths['base_theme'],
                 enabled_theme=file_paths['enabled_theme'])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='zookeepr', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.app_globals'] = app_globals.Globals()
    config['pylons.h'] = zookeepr.lib.helpers

    # Create the Mako TemplateLookup, with the default auto-escaping
    config['pylons.app_globals'].mako_lookup = TemplateLookup(
        directories=[paths['enabled_theme'], paths['default_theme']],
        error_handler=handle_mako_error,
        module_directory=os.path.join(app_conf['cache_dir'], 'templates'),
        input_encoding='utf-8', default_filters=['escape'],
        imports=['from webhelpers.html import escape'])

    # Setup the SQLAlchemy database engine
    engine = engine_from_config(config, 'sqlalchemy.')
    init_model(engine)

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)
