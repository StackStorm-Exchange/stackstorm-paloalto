from .lib.actions import BaseAction


class BulkDeleteObjects(BaseAction):
    """
    Delete objects from a firewall in bulk
    """
    def run(self, class_string, device_group, firewall, objects):

        device = self.get_panorama(firewall, device_group)
        pandevice_class = self.get_pandevice_class(class_string)
        cls = pandevice_class['cls']

        # because we are bulk deleting, we do not refresh the object tree

        for obj in objects:
            pandevice_object = cls(name=str(obj))
            device.add(pandevice_object)

        pandevice_object.delete_similar()

        device_value = device_group or firewall
        return True, "{} objects successfully deleted from {}".format(cls.__name__, device_value)
