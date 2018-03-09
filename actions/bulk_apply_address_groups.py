from pandevice.objects import AddressGroup

from lib.actions import BaseAction


class BulkApplyAddressGroup(BaseAction):
    """
    Add/update address groups to a firewall in bulk
    """
    def run(self, device_group, firewall, objects):

        valid_keys = set(['name', 'description', 'static_value', 'description', 'dynamic_value', 'tag'])

        device = self.get_panorama(firewall, device_group)
        for obj in objects:
            if not isinstance(obj, dict):
                raise ValueError("{} is not a valid AddressGroup object!".format(obj))
            if not set(obj.keys()).issubset(valid_keys):
                raise ValueError("{} contains invalid values for an AddressGroup object!".format(obj))

            address_group_obj = AddressGroup(**obj)
            device.add(address_group_obj)

        address_group_obj.apply_similar()

        device_value = device_group or firewall
        return True, "AddressGroups successfully applied to {}".format(device_value)
