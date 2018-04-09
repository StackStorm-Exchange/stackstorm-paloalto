from lib.actions import BaseAction


class Commit(BaseAction):
    """
    Commit a firewall
    """
    def run(self, firewall, sync, exception):

        device = self.get_pandevice(firewall)

        try:
            device.commit(sync=sync, exception=exception)
        except Exception as e:
            return False, "Commit on {} rasied exception: {}".format(firewall, e)

        if not sync:
            return True, "Commit on {} successfully requested!".format(firewall)

        return True, "Commit on {} successfully completed!".format(firewall)
