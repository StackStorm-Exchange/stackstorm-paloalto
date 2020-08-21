from lib.base import BaseAction

# Defines the methods that a given endpoint has in pan-python
# (used for validation prior to execution)
API_METHOD_LIST = ['submit',
                   'change_request',
                   'sample',
                   'report',
                   'verdict',
                   'verdicts',
                   'verdicts_changed',
                   'pcap',
                   'testfile']

# The fields available for building the connection with this API endpoint
# (used for validation prior to connection)
#                        (key, required, default)
CONNECTION_FIELDS = [('tag', False, None),
                     ('hostname', True, 'wildfire.paloaltonetworks.com'),
                     ('api_key', False, None),
                     ('http', False, False),
                     ('timeout', False, None),
                     ('ssl_context', False, None)]

module = "pan.wfapi"
module_class = "PanWFapi"


class Action(BaseAction):

    def run(self, **kwargs):

        # Basic housekeeping for runnign the action
        self.action_setup(API_METHOD_LIST, **kwargs)

        # Create the connection for the api
        result = self.api_client(module, module_class, CONNECTION_FIELDS)

        if result:
            return self.format_action_result(response_data=result,
                                             succeeded=True,
                                             response_msg='')
