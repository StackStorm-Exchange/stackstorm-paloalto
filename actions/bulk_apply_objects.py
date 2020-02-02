from .lib.actions import BaseAction


class BulkApplyObjects(BaseAction):
    """
    Add/update objects to a firewall in bulk
    """
    def run(self, class_string, device_group, firewall, objects):

        device = self.get_panorama(firewall, device_group)
        pandevice_class = self.get_pandevice_class(class_string)
        cls = pandevice_class['cls']
        cls.refreshall(parent=device)

        for obj in objects:
            if not isinstance(obj, dict):
                raise ValueError("{} is not a valid {} object!".format(obj, cls.__name__))
            if not set(obj.keys()).issubset(set(pandevice_class['valid_keys'])):
                raise ValueError(
                    "{} contains invalid values for an {} object!".format(obj, cls.__name__)
                )

            # manually update an existing object or add a new one
            pandevice_object = device.find(obj['name'], class_type=cls)
            if pandevice_object is not None:
                for key, value in obj.items():
                    setattr(pandevice_object, key, value)

            else:
                pandevice_object = cls(**obj)
                device.add(pandevice_object)

        pandevice_object.apply_similar()

        device_value = device_group or firewall
        return True, "{} objects successfully applied to {}".format(cls.__name__, device_value)
