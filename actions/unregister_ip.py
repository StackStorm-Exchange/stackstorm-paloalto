"""
    This action is deprecated and will be removed in a future release
"""

from lib.actions import BaseAction


class UnregisterIP(BaseAction):
    """
    Unregister IP/tag(s) to a firewall
    """
    def run(self, ip, tag, tag_list, firewall):

        if not tag and not tag_list:
            return False, "You must specify either tag or tag_list!"

        if tag and tag_list:
            return False, "You must only specify either tag OR tag_list but not both!"

        unregister_tag = tag or tag_list

        device = self.get_pandevice(firewall)

        device.userid.unregister(ip, unregister_tag)

        return True, "{} successfully unregistered to {}".format(",".join(unregister_tag), ip)
