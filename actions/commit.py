from pandevice.panorama import Panorama

from lib.actions import BaseAction


class Commit(BaseAction):
    """
    Commit a firewall
    """
    def run(self, firewall, device_group, sync, sync_all, exception):

        device = self.get_pandevice(firewall)
        if device_group and not isinstance(device, Panorama):
            raise ValueError(
                '{} is not a Panorama and does not understand device_group!'.format(firewall)
            )

        if isinstance(device, Panorama):
            try:
                device.commit(sync=sync, exception=exception)
                device.commit_all(sync=sync,
                                  sync_all=sync_all,
                                  devicegroup=device_group,
                                  exception=exception)
            except Exception as e:
                return False, "Commit on {} rasied exception: {}".format(firewall, e)
        else:
            try:
                device.commit_all(sync=sync, exception=exception)
            except Exception as e:
                return False, "Commit on {} rasied exception: {}".format(firewall, e)

        if not sync:
            return True, "Commit on {} successfully requested!".format(firewall)

        return True, "Commit on {} successfully completed!".format(firewall)
