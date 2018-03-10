from lib.actions import BaseAction


class RegisterIP(BaseAction):
    """
    Register IP/tag(s) to a firewall
    """
    def run(self, ip, tag, tag_list, firewall):

        if not tag and not tag_list:
            return False, "You must specify either tag or tag_list!"

        if tag and tag_list:
            return False, "You must only specify either tag OR tag_list but not both!"

        register_tag = tag or tag_list

        device = self.get_pandevice(firewall)

        device.userid.register(ip, register_tag)

        return True, "{} successfully registered to {}".format(",".join(register_tag), ip)
