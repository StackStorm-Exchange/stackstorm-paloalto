from pandevice.panorama import Panorama

from .lib.actions import BaseAction


class CommitAll(BaseAction):
    """
    Commit All on a Panorama
    """
    def run(self, firewall, device_group, sync, sync_all, exception):

        device = self.get_pandevice(firewall)

        if not isinstance(device, Panorama):
            return False, "Device is not a Panorama!"

        if sync_all and not sync:
            return False, "You must use 'sync' in order to use 'sync_all'."

        try:
            device.commit_all(
                sync=sync,
                sync_all=sync_all,
                devicegroup=device_group,
                exception=exception
            )
        except Exception as e:
            return False, "Commit on {} rasied exception: {}".format(firewall, e)

        if not sync:
            return True, "Commit on {} successfully requested!".format(firewall)

        return True, "Commit on {} successfully completed!".format(firewall)
