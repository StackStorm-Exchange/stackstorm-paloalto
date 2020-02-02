import json

from .lib.actions import BaseAction


class GetObject(BaseAction):
    """
    Get object(s) from a device. If serialize is true, convert the object(s) to
    dicts and then to json
    """
    def run(self, class_string, name, serialize, device_group, firewall, **kwargs):

        device = self.get_panorama(firewall, device_group)
        cls = self.get_pandevice_class(class_string)['cls']
        keys = self.get_pandevice_class(class_string)['valid_keys']
        cls.refreshall(device)

        if name:
            obj = device.find(name, cls)
        else:
            obj = device.findall(cls)

        if serialize:
            if isinstance(obj, list):
                data = []
                for o in obj:
                    serialized_obj = {}
                    for key in keys:
                        serialized_obj[key] = getattr(o, key)
                    data.append(serialized_obj)
            else:
                data = {}
                for key in keys:
                    data[key] = getattr(obj, key)

            return json.dumps(data)
        else:
            return obj
