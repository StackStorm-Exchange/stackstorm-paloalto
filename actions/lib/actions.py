from pandevice.base import PanDevice
from pandevice.errors import PanDeviceError
from pandevice.panorama import Panorama, DeviceGroup

from st2common.runners.base_action import Action


class BaseAction(Action):
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
            raise Exception("Failed to connect to firewall {} with pandevice error {}".format(firewall_config, e))

        return device.refresh()

    def get_panorama(self, firewall, device_group):
        """
        If the device is a Panorama and device_group is passed, return the device group else just return the device.
        """
        device = self.get_pandevice(firewall)
        if device_group:
            if not isinstance(device, Panorama):
                raise Exception("Device {} is not a Panorama!".format(firewall))

            device.refresh_devices(add=True)
            device = device.find(device_group, DeviceGroup)
            if device is None:
                raise Exception("DeviceGroup {} does not exist on device {}!".format(device_group, firewall))
            device.refresh()

        return device
