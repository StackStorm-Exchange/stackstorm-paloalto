from pandevice.policies import Rulebase, PreRulebase, PostRulebase

from lib.actions import BaseAction


class ApplySingleObject(BaseAction):
    """
    Apply an object to a device
    """
    def run(self, class_string, device_group, firewall, pre_rulebase, **kwargs):

        device = self.get_panorama(firewall, device_group)
        pandevice_class = self.get_pandevice_class(class_string)
        cls = pandevice_class['cls']
        obj = cls(**kwargs)

        # we need some special logic for policies
        if device_group and pre_rulebase:
            rulebase = PreRulebase()
        elif device_group and not pre_rulebase:
            rulebase = PostRulebase()
        else:
            rulebase = Rulebase()

        device.add(rulebase)
        rulebase.add(obj)
        obj.apply()

        device_value = device_group or firewall
        return True, "{} {} successfully applied to {}".format(cls.__name__, obj.name, device_value)
