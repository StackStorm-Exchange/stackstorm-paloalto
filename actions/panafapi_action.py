from lib.base import BaseAction

# Defines the methods that a given endpoint has in pan-python
# (used for validation prior to execution)
API_METHOD_LIST = ['samples_search',
                   'samples_results',
                   'samples_search_results',
                   'sessions_search',
                   'sessions_results',
                   'sessions_search_results',
                   'sessions_histogram_search',
                   'sessions_histogram_results',
                   'sessions_histogram_search_results',
                   'sessions_aggregate_search',
                   'sessions_aggregate_results',
                   'sessions_aggregate_search_results',
                   'top_tags_search',
                   'top_tags_results',
                   'top_tags_search_results']

# The fields available for building the connection with this API endpoint
# (used for validation prior to connection)
#                    (key, required, default)
CONNECTION_FIELDS = [('api_version', False, None),
                     ('hostname', True, 'autofocus.paloaltonetworks.com'),
                     ('api_key', False, None),
                     ('panrc_tag', False, None),
                     ('timeout', False, None),
                     ('verify_cert', False, True),
                     ('sleeper', False, None)]

module = "pan.afapi"
module_class = "PanAFapi"


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
