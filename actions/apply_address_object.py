from pandevice.objects import AddressObject

from lib.actions import BaseAction


class ApplyAddressObject(BaseAction):
    """
    Add/update address object to a firewall
    """
    def run(self, device_group, firewall, **kwargs):

        device = self.get_panorama(firewall, device_group)
        obj = AddressObject(**kwargs)
        device.add(obj)
        obj.apply()

        device_value = device_group or firewall
        return True, "AddressObject {} successfully applied to {}".format(obj.name, device_value)
