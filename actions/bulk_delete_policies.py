"""
    This action is deprecated and will be removed in a future release
"""

from pandevice.policies import Rulebase, PreRulebase, PostRulebase

from lib.actions import BaseAction


class BulkDeletePolicies(BaseAction):
    """
    Delete policies from a firewall in bulk
    """
    def run(self, class_string, device_group, firewall, objects, pre_rulebase):

        device = self.get_panorama(firewall, device_group)
        pandevice_class = self.get_pandevice_class(class_string)
        cls = pandevice_class['cls']

        # we need some special logic for policies
        if device_group and pre_rulebase:
            rulebase = PreRulebase()
        elif device_group and not pre_rulebase:
            rulebase = PostRulebase()
        else:
            rulebase = Rulebase()

        device.add(rulebase)

        # because we are deleting in bulk, we do not refresh the object tree

        for obj in objects:
            if not isinstance(obj, str):
                raise ValueError("{} is not a valid {} object name!".format(obj, cls.__name__))

            pandevice_object = cls(name=obj)
            rulebase.add(pandevice_object)

        pandevice_object.delete_similar()

        device_value = device_group or firewall
        return True, "{} objects successfully deleted from {}".format(cls.__name__, device_value)
