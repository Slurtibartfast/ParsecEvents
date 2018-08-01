from configparser import ConfigParser
from uuid import UUID

import constants
import xtensions


class transport:
    server_guid = UUID.empty()
    local_guid = UUID.empty()
    server_path = ""
    server_port = 0
    local_path = ""
    local_port = 0


class parsec_server:
    server_address = ""
    server_entry = ""
    client_address = ""
    remote_data_start_port = 0


class events:
    mutex = ""
    event_name = ""
    data = ""


class hal:
    mutex = ""
    pnp_event_name = ""
    data = ""
    udp_send_timeout = 0
    udp_max_attempt = 0


class hal_lookup:
    data = ""


class ui:
    mutex = ""
    data = ""


class tasksched:
    mutex = ""
    event_name = ""
    data = ""


class cache:
    mutex = ""
    data = ""


class encryption:
    enabled = False


class file_exchange:
    server_ip = ""
    server_port = 22
    user = ""
    password = ""
    home_dir = ""
    enabled = False
    exchange_directory = ""
    server_protocol = ""


def __read():
    config = ConfigParser()

    print(constants.parsec_directory + 'parsec.ini')

    # parse existing file
    config.read(constants.parsec_directory + 'parsec.ini')

    transport_section = "Transport"
    value = config.get(transport_section, "ServerGuid", fallback="")
    transport.server_guid = UUID(value) if len(value) > 0 else UUID.empty()
    value = config.get(transport_section, "LocalGuid", fallback="")
    transport.local_guid = UUID(value) if len(value) > 0 else UUID.empty()
    transport.server_path = config.get(transport_section, "ServerPath")
    value = config.get(transport_section, "ServerPort", fallback="")
    transport.server_port = int(value) if len(value) > 0 else 0
    transport.local_path = config.get(transport_section, "LocalPath")
    value = config.get(transport_section, "LocalPort", fallback="")
    transport.local_port = int(value) if len(value) > 0 else 0

    parsec_server_section = "ParsecServer"
    parsec_server.server_address = config.get(parsec_server_section, "ServerAddress")
    parsec_server.server_entry = config.get(parsec_server_section, "ServerEntry")
    parsec_server.client_address = config.get(parsec_server_section, "ClientAddress")
    value = config.get(parsec_server_section, "RemoteDataStartPort", fallback="")
    parsec_server.remote_data_start_port = int(value) if len(value) > 0 else 0

    events_section = "Events"
    events.mutex = config.get(events_section, "mutex")
    events.event_name = config.get(events_section, "eventName")
    events.data = config.get(events_section, "data")

    hal_section = "Hal"
    hal.mutex = config.get(hal_section, "mutex")
    hal.pnp_event_name = config.get(hal_section, "pnpEventName")
    hal.data = config.get(hal_section, "data")
    value = config.get(hal_section, "UdpSentTimeout", fallback="")
    hal.udp_send_timeout = int(value) if len(value) > 0 else 0
    value = config.get(hal_section, "UdpMaxAttempt", fallback="")
    hal.udp_max_attempt = int(value) if len(value) > 0 else 0

    hal_lookup_section = "Hal_Lookup"
    hal_lookup.data = config.get(hal_lookup_section, "data")

    ui_section = "UI"
    ui.mutex = config.get(ui_section, "mutex")
    ui.data = config.get(ui_section, "data")

    tasksched_section = "Tasksched"
    tasksched.mutex = config.get(tasksched_section, "mutex")
    tasksched.event_name = config.get(tasksched_section, "eventName")
    tasksched.data = config.get(tasksched_section, "data")

    cache_section = "Cache"
    cache.mutex = config.get(cache_section, "mutex")
    cache.data = config.get(cache_section, "data")

    encryption_section = "Encryption"
    value = config.get(encryption_section, "enable", fallback="")
    encryption.enabled = bool(value) if len(value) > 0 else False

    file_exchange_section = "FileExchange"
    file_exchange.server_ip = config.get(file_exchange_section, "ServerIp")
    value = config.get(file_exchange_section, "ServerPort", fallback="")
    file_exchange.server_port = int(value) if len(value) > 0 else 0
    file_exchange.user = config.get(file_exchange_section, "User")
    file_exchange.password = config.get(file_exchange_section, "Password")
    file_exchange.home_dir = config.get(file_exchange_section, "HomeDir")
    value = config.get(file_exchange_section, "Enabled", fallback="")
    file_exchange.enabled = bool(value) if len(value) > 0 else False
    file_exchange.exchange_directory = config.get(file_exchange_section, "ExchangeDirectory")


__read()
