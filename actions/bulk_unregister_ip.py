from .lib.actions import BaseAction


class BulkUnregisterIP(BaseAction):
    """
    Register IP/tag(s) to a firewall
    """
    def run(self, objects, firewall):

        valid_keys = set(['ip', 'tag', 'tag_list'])

        device = self.get_pandevice(firewall)
        device.userid.batch_start()

        for obj in objects:
            if not isinstance(obj, dict):
                raise ValueError("{} is not a valid unregister ip object!".format(obj))
            if not set(obj.keys()).issubset(valid_keys):
                raise ValueError("{} contains invalid values for unregister ip object!".format(obj))

            register_tag = obj.get('tag') or obj.get('tag_list')
            device.userid.unregister(obj.get('ip'), register_tag)

        device.userid.batch_end()

        return True, "Successfully unregistered IPs/tags to {}".format(firewall)
