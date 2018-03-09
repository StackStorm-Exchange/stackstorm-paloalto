from pandevice.objects import AddressObject

from lib.actions import BaseAction


class BulkApplyAddressObjects(BaseAction):
    """
    Add/update address objects to a firewall in bulk
    """
    def run(self, device_group, firewall, objects):

        valid_keys = set(['name', 'description', 'value', 'type', 'tag'])

        device = self.get_panorama(firewall, device_group)
        for obj in objects:
            if not isinstance(obj, dict):
                raise ValueError("{} is not a valid Address object!".format(obj))
            if not set(obj.keys()).issubset(valid_keys):
                raise ValueError("{} contains invalid values for an Address object!".format(obj))

            address_obj = AddressObject(**obj)
            device.add(address_obj)

        address_obj.apply_similar()

        device_value = device_group or firewall
        return True, "AddressObjects successfully applied to {}".format(device_value)
