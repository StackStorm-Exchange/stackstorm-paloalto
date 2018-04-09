from pandevice.base import PanDevice
from pandevice.errors import PanDeviceError
from pandevice.panorama import Panorama, DeviceGroup
from pandevice import objects
from pandevice.policies import SecurityRule

from st2common.runners.base_action import Action


class BaseAction(Action):

    PANDEVICE_CLASSES = {
        'AddressObject': {
            'cls': objects.AddressObject,
            'valid_keys': [
                'name', 'description', 'value', 'type', 'tag'
            ],
        },
        'AddressGroup': {
            'cls': objects.AddressGroup,
            'valid_keys': [
                'name', 'description', 'static_value', 'dynamic_value', 'tag'
            ],
        },
        'ServiceObject': {
            'cls': objects.ServiceObject,
            'valid_keys': [
                'name', 'protocol', 'source_port', 'destination_port', 'description', 'tag'
            ],
        },
        'ServiceGroup': {
            'cls': objects.ServiceGroup,
            'valid_keys': [
                'name', 'value', 'tag'
            ],
        },
        'SecurityRule': {
            'cls': SecurityRule,
            'valid_keys': [
                'name', 'description', 'nat_type', 'fromzone', 'tozone', 'source', 'destination',
                'application', 'service', 'category', 'action', 'log_setting', 'log_start',
                'log_end', 'description', 'type', 'tag', 'negate_source', 'negate_destination',
                'disabled', 'schedule', 'icmp_unreachable', 'disable_server_response_inspection',
                'group', 'virus', 'spyware', 'vulnerability', 'url_filtering', 'file_blocking',
                'wildfire_analysis', 'data_filtering', 'negate_target', 'target',
            ],
        },
    }

    def __init__(self, config):
        super(BaseAction, self).__init__(config)
        if config is None:
            raise ValueError("No connection configuration details found")
        if "firewall" in config:
            if config['firewall'] is None:
                raise ValueError("'firewall' config defined but empty.")
            else:
                pass
        else:
            raise ValueError("No connection configuration details found")

    def get_pandevice(self, firewall):
        if firewall:
            firewall_config = self.config['firewall'].get(firewall)
        else:
            firewall_config = self.config['firewall'].get('default')

        # no need to duplicate config validation because pandevice is verbose enough
        device = None
        try:
            device = PanDevice.create_from_device(
                hostname=firewall_config.get('host'),
                api_username=firewall_config.get('api_username'),
                api_password=firewall_config.get('api_password'),
                api_key=firewall_config.get('api_key'),
                port=firewall_config.get('port'),
            )
        except PanDeviceError as e:
            raise Exception(
                "Failed to connect to firewall {} with pandevice error {}".format(firewall_config,
                                                                                  e)
            )

        return device

    def get_panorama(self, firewall, device_group):
        """
        If the device is a Panorama and device_group is passed, return the device group else
        just return the device.
        """
        device = self.get_pandevice(firewall)
        if device_group:
            if not isinstance(device, Panorama):
                raise Exception("Device {} is not a Panorama!".format(firewall))

            device.refresh_devices(add=True)
            device = device.find(device_group, DeviceGroup)
            if device is None:
                raise Exception(
                    "DeviceGroup {} does not exist on device {}!".format(device_group, firewall)
                )

        return device

    def get_pandevice_class(self, class_string):
        return self.PANDEVICE_CLASSES.get(class_string)
