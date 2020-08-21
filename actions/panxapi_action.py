from lib.base import BaseAction


# Defines the methods that a given endpoint has in pan-python
# (used for validation prior to execution)
API_METHOD_LIST = ['show',
                   'get',
                   'delete',
                   'set',
                   'edit',
                   'move',
                   'rename',
                   'clone',
                   'override',
                   'op',
                   'user_id',
                   'ad_hoc',
                   'keygen',
                   'commit',
                   'export',
                   'log',
                   'report']

# The fields available for building the connection with this API endpoint
# (used for validation prior to connection)
#                    (key, required, default)
CONNECTION_FIELDS = [('tag', False, None),
                     ('hostname', True, None),
                     ('api_username', False, None),
                     ('api_password', False, None),
                     ('api_key', False, None),
                     ('port', False, None),
                     ('serial', False, None),
                     ('use_http', False, False),
                     ('use_get', False, False),
                     ('timeout', False, None),
                     ('ssl_context', False, None)]

DEFAULT_EXPORT_PATH = '/temp_files'

module = "pan.xapi"
module_class = "PanXapi"


class Action(BaseAction):

    def run(self, **kwargs):
        """ Primary Action for XApi. Other methods may have a one off action
        """

        xml_result = kwargs.pop('xml_result', False)
        download_to = kwargs.pop('download_to', None)

        # Basic housekeeping for runnign the action
        self.action_setup(API_METHOD_LIST, **kwargs)

        # Create the connection for the api
        self.api_client(module, module_class, CONNECTION_FIELDS)

        # Sometimes the response data is a file that will be stored in self.client.export_result
        # if there is a file there
        if self.client.export_result:
            self._export_file(export_file_data=self.client.export_result['content'],
                              export_file_name=self.client.export_result['file'],
                              export_file_path=download_to)

            # This should never be used since _export_file() should handle returning data
            return True

        # Check if the action requested the result in XML format
        if xml_result:
            # Run the xml_result() method that is part of PanXapi
            # ( pan.xapi.PanXapi.xml_result() )
            result = self.client.xml_result()

            if result:
                return self.format_action_result(response_data=result,
                                                 succeeded=True,
                                                 response_msg='')

        else:
            # Return Python Object that is iterable
            # Run the pan_config() method in base.lib (pan.config.PanConfig)
            # and then return the results of  pan.config.PanConfig.python()
            result = self.pan_config(config=self.client).python()

            if result:
                return self.format_action_result(response_data=result,
                                                 succeeded=True,
                                                 response_msg='')

    def _export_file(self, export_file_data=None, export_file_name=None, export_file_path=None):

        export_file_data = self.client.export_result['content']
        export_file_name = self.client.export_result['file']

        # Check if there is a download path to be used.
        if export_file_path:
            result = self.download_file(file_path=export_file_path,
                                        file_name=export_file_name,
                                        data=export_file_data)

        else:
            export_file_path = DEFAULT_EXPORT_PATH
            result = self.download_file(file_path=export_file_path,
                                        file_name=export_file_name,
                                        data=export_file_data)

        full_file_path = '{}/{}'.format(export_file_path, export_file_name)

        if result:
            return self.format_action_result(response_data=full_file_path,
                                             succeeded=True,
                                             response_msg='file successfully created')
        else:

            return self.format_action_result(response_data=full_file_path,
                                             succeeded=False,
                                             response_msg='file could not be created')
