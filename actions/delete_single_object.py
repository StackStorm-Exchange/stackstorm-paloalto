from .lib.actions import BaseAction


class DeleteSingleObject(BaseAction):
    """
    Delete an object from a device
    """
    def run(self, class_string, device_group, firewall, **kwargs):

        device = self.get_panorama(firewall, device_group)
        cls = self.get_pandevice_class(class_string)['cls']
        obj = cls(**kwargs)
        device.add(obj)
        obj.delete()

        device_value = device_group or firewall
        return True, "{} {} successfully deleted from {}".format(
            cls.__name__, obj.name, device_value
        )
