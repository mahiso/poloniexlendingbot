from coinlendingbot.plugins import *

config = None
api = None
log = None
notify_conf = None
plugins = []


def init_plugin(plugin_name):
    """
        :return: instance of requested class
        :rtype: Plugin
        """
    klass = globals()[plugin_name]  # type: Plugin
    instance = klass(config, api, log, notify_conf)
    instance.on_bot_init()
    return instance


def init(cfg, api1, log1, notify_conf1):
    """
    @type cfg1: modules.Configuration
    @type api1: modules.Poloniex.Poloniex
    @type log1: modules.Logger.Logger
    """
    global config, api, log, notify_conf
    config = cfg
    api = api1
    log = log1
    notify_conf = notify_conf1

    plugin_names = config.get_plugins_config()
    active_plugins = []
    for plugin_name in plugin_names:
        try:
            plugins.append(init_plugin(plugin_name))
            active_plugins.append(plugin_name)
        except Exception as ex:
            log.log_error('Failed to load plugin {}: {}'.format(plugin_name, ex.message))

    log.addSectionLog("plugins", "enabled", active_plugins)


def after_lending():
    for plugin in plugins:
        plugin.after_lending()


def before_lending():
    for plugin in plugins:
        plugin.before_lending()


def on_bot_exit():
    for plugin in plugins:
        plugin.on_bot_stop()
