"""
    This action is deprecated and will be removed in a future release
"""

from lib.actions import BaseAction


class BulkRegisterIP(BaseAction):
    """
    Register IP/tag(s) to a firewall
    """
    def run(self, objects, firewall):

        valid_keys = set(['ip', 'tag', 'tag_list'])

        device = self.get_pandevice(firewall)
        device.userid.batch_start()

        for obj in objects:
            if not isinstance(obj, dict):
                raise ValueError("{} is not a valid register ip object!".format(obj))
            if not set(obj.keys()).issubset(valid_keys):
                raise ValueError("{} contains invalid values for register ip object!".format(obj))

            register_tag = obj.get('tag') or obj.get('tag_list')
            device.userid.register(obj.get('ip'), register_tag)

        device.userid.batch_end()

        return True, "Successfully registered IPs/tags to {}".format(firewall)
