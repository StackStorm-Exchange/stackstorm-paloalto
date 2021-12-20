from lib.base import BaseAction
import sys

# Defines the methods that a given endpoint has in pan-python
# (used for validation prior to execution)
API_METHOD_LIST = ['activate',
                   'deactivate',
                   'get']
# The fields available for building the connection with this API endpoint
# (used for validation prior to connection)
#                        (key, required, default)
CONNECTION_FIELDS = [('api_version', False, None),
                     ('hostname', True, 'api.paloaltonetworks.com'),
                     ('api_key', False, None),
                     ('panrc_tag', False, None),
                     ('timeout', False, None),
                     ('verify_cert', False, True)]

module = "pan.licapi"
module_class = "PanLicapi"


class Action(BaseAction):

    def run(self, **kwargs):
        """ Execute the action
        """

        # Basic housekeeping for runnign the action
        self.action_setup(API_METHOD_LIST, **kwargs)

        # Create the connection for the api
        result = self.api_client(module, module_class, CONNECTION_FIELDS)

        try:
            result.raise_for_status()
        except self.imported_error_module as msg:
            self.logger.error(
                '{}: {}').format(self.api_method, msg)
            sys.exit(1)

        if result.json:
            return self.format_action_result(response_data=result.json,
                                             succeeded=True,
                                             response_msg='')
