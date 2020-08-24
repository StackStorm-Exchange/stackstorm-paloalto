from st2common.runners.base_action import Action
from importlib import import_module

import sys
import six
import json
import os


class BaseAction(Action):
    """ The base class for all actions
    """

    def __init__(self, config):
        """ init method, run at class creation
        """
        super(BaseAction, self).__init__(config)
        self.logger.debug('Instantiating BaseAction()')

    def api_client(self, module=None, module_class=None, connection_fields=None):
        """ client for all API Endpoints for the pack.
            XAPI (Devices), Wildfire, Autofocus, Licensing (Cloud)
        """

        if not connection_fields:
            raise ValueError(
                'connection_fields are required, but received {}'.format(connection_fields))

        self.logger.debug(
            'Loading Class {} for Module {}'.format(module_class, module))
        self._import_module_class(module, module_class)

        connection = self._setup_connection(connection_fields)

        # Parameter clean up and housekeeping
        self._parameter_housekeeping(**self.action_kwargs)

        # ADD CHECK and METHOD for if extra_qs is a string or dict, and convert to dict
        if 'extra_qs' in self.action_kwargs and self.action_kwargs['extra_qs']:
            self.action_kwargs['extra_qs'] = self.parse_extra_qs(
                data=self.action_kwargs['extra_qs'])

        self.logger.debug(
            'Initializing api client on {} for host: {}'.format(module, connection['hostname']))
        try:
            self.client = getattr(self.imported_module,
                                  module_class)(**connection)
        except Exception as err:
            self.logger.error(err)
            sys.exit(1)

        try:
            result = getattr(self.client, self.api_method)(**self.action_kwargs)
        except Exception as err:
            self.logger.error(err)
            sys.exit(1)

        # some modules return the result of the method, some assign the result to a class object.
        # We return for the cases that want it, and cases that don't, don't care.
        return result

    def netmiko_client(self, host=None, username=None, password=None):
        """ Handles the setup and connection when using the netmiko_client
        """
        # Import the module when this method is called.
        from netmiko import ConnectHandler

        # Validate inputs
        if not host:
            raise ValueError('netmiko_client(host) is required, but no value received')
        if not username:
            raise ValueError('netmiko_client(username) is required, but no value received')
        if not password:
            raise ValueError('netmiko_client(password) is required, but no value received')

        # Format the Netmiko request
        host_profile = {'device_type': 'paloalto_panos',
                        'username': username,
                        'password': password,
                        'host': host,
                        'timeout': 15}
        self.logger.debug(
            'Initializing netmiko client on host: {} with user: {}***{}'.format(
                host, username[:1], username[-2:]))

        try:
            connection = ConnectHandler(**host_profile)
            # connection = PaloAltoPanosBase(**host_profile)
        except Exception as e:
            self.logger.error(e)
            sys.exit(1)
        else:
            return connection

    def pan_config(self, config=None):
        """ The XApi Endpoint needs to have the data returned ran through a special method that parses it
            into useful data.
        """

        if not config:
            raise ValueError(
                'config is a required object for pan_config(), recieved: "{}"'.format(config))

        # import here so we don't bother unless its needed
        from pan.config import PanConfig
        from pan.config import PanConfigError

        # Format useful output from XML for the element_root
        # https://github.com/kevinsteves/pan-python/blob/master/doc/pan.xapi.rst#element_root
        try:
            result = PanConfig(config=config.element_root)
        except PanConfigError as msg:
            self.logger.error(
                'pan.config.PanConfigError: {}'.format(msg))
        else:
            return result

    def retieve_config_connection(self, connection_name=None):
        """ Checks the pack config for a named connection entry
            and returns a dict with connection params from config entry.
            If no config found, returns an empty dict {}
        """

        try:
            config_connection = self.config['connections'].get(
                connection_name, None)
        except Exception as err:
            self.logger.error(
                'Specified connection "{}" Error: {}'.format(connection_name, err))
            sys.exit(1)
        # If we found a valid config (not None), set it as the connection
        if config_connection:
            self.logger.debug(
                'Connection with name "{}"" loaded from pack configuration'.format(connection_name))
            return config_connection
        # didn't find the connection_name in the config
        else:
            self.logger.warning(
                'Connection with name "{}" not found in configuration'.format(connection_name))
            # return an empty dictionary
            connection = {}
            return connection

    def action_setup(self, api_method_list, **kwargs):
        """ Takes care of all the setup and validation that needs to be done before trying
            the API Client method api_client()
        """

        self.api_method = kwargs.pop('api_method', None)

        # Check that the method we are attempting to use is in the list of valid methods
        if self.api_method not in api_method_list:
            raise KeyError(
                'api_method is a required parameter and must be one of "{}" \
                Method Supplied: {}'.format(api_method_list, self.api_method))

        self.logger.debug(
            'API Method: {}'.format(self.api_method))

        self.connection_name = kwargs.pop('connection_name', None)

        # Assign kwargs to a class object so its easy to manipulate later
        self.action_kwargs = kwargs

        return True

    def parse_extra_qs(self, data=None):
        """ Parses the value from the parameter `extra_qs`.
            Either loads a JSON String into a dict, or parses a
            string of kwargs into a dict.
        """

        if not data:
            self.logger.debug(
                'data is a required field for parse_extra_qs()')

        try:
            json.loads(data)
        except Exception:
            pass
        else:
            return json.loads(data)

        kwarg_dict = {}
        kwarg_list = data.split('&')
        for kwarg in kwarg_list:
            if '=' in kwarg:
                k = kwarg.split('=')[0]
                v = kwarg.split('=')[1]
                kwarg_dict[k] = v

        if not kwarg_dict:
            self.logger.debug(
                'no parsable kwargs found in extra_qs, please check your formatting')

        return kwarg_dict

    def download_file(self, file_path=None, file_name=None, data=None):
        """ Handles downloading a file to the supplied path
        """

        if file_path[-1:] != '/':
            file_path = '{}/'.format(file_path)

        file = '{}{}'.format(file_path, file_name)

        if not os.path.exists(file_path):
            os.makedirs(file_path)
            self.logger.debug(
                'Path {} does not exist. Creating.'.format(file_path))

        try:
            os.access(file_path, os.W_OK)
        except Exception as e:
            self.logger.error('File path {} Error: {}'.format(file_path, e))
            return False

        with open(file, 'wb') as f:
            try:
                # f.write(bytearray(int(i, 16) for i in data))
                f.write(data)
            except Exception as e:
                self.logger.error('Error when attempting to write data to file: {}'.format(e))
                return False

        return True

    def format_action_result(self, response_data=None,
                             succeeded=None, response_msg=None):
        """ Handles formatting to ensure consistent results formatting
        """
        return {'data': response_data,
                'succeeded': succeeded,
                'response_msg': response_msg}

    def _setup_connection(self, connection_fields):
        """ Handles the logic for determining what credentials/hostname to use.
            Resolves conflicts between config values, and action values

            Credential priority: API Key > User/Pass
            General Priority: Action Specified Value > Config Value
        """

        if not self.action_kwargs:
            self.logger.error(
                'action_setup() is required to be ran prior to _setup_connection()')
            sys.exit(1)

        # dict to either replace with a config connection, or load Action values into
        connection = {}

        if self.connection_name:
            connection = self.retieve_config_connection(connection_name=self.connection_name)

        # Evaluate the connection fields provided for this specific API Endpoint (xapi, wfapi, etc)
        for key, required, default in connection_fields:
            # Prefer values found from the action Over the ones from the config
            if self.action_kwargs.get(key, None) not in [None, '']:
                connection[key] = self.action_kwargs.pop(key)
                continue
            elif connection and key in connection:
                if connection[key] or connection[key] is False:
                    pass
            # If we haven't found the key yet, check if its required
            elif required:
                # False is potentially a valid default value for a boolean
                if default or default is False:
                    self.logger.debug(
                        'Value for Key "{}" not provided, but default is specified ({})'.format(
                            key, default))
                    connection[key] = default
                # No usable default or value passed, time to fail.
                else:
                    raise ValueError(
                        'Required Parameter "{}" missing.'.format(key))

            # If the key is still in action_kwargs and its related to connection, remove it.
            if key in self.action_kwargs:
                del self.action_kwargs[key]

        if 'api_key' in connection and connection['api_key']:
            self.logger.debug(
                'Connection setup using API Key: "{}***{}"'.format(
                    connection['api_key'][:1], connection['api_key'][-5:]))
        else:
            self.logger.debug(
                'Connection setup using User: "{}***{}"'.format(
                    connection['api_username'][:1], connection['api_username'][-2:]))

        return connection

    def _import_module_class(self, module=None, module_class=None):
        """ Handles importing of modules and classes as needed based on the API required
            for the action. This increases efficency as we dont have to load every
            module/class every time
        """

        if not module or not module_class:
            raise ValueError(
                'module and module_class is required, but received {}, {}'.format(
                    module, module_class))
        # Import the Class for the API endpoint (PanXapi)
        try:
            self.imported_module = import_module(module, package=module_class)
            # Static Example: from pan.xapi import PanXapi
        except Exception as err:
            self.logger.error(
                'Failed to import class: "{}" in module: "{}" Error: {}'.format(
                    module_class, module, err))
            sys.exit(1)
        # Import the 'Error' class (PanXapiError)
        try:
            self.imported_error_module = import_module(
                module, module_class + 'Error')
            # Static Example: from pan.xapi import PanXapiError
        except Exception as err:
            self.logger.error(
                'Failed to import class: "{}" in module: "{}" Error: {}'.format(
                    module_class + 'Error', module, err))
            sys.exit(1)

    def _parameter_housekeeping(self, **kwargs):
        """ Modify special case action parameters

            We need to be able to permanently modify self.action_kwargs based on any
            matched conditions. Python doesn't like it when you modify length or size
            of a dictionary while its trying to iterate over it, so we create a copy
            to iterate over, while modifying the true source.
            Usually this is not the best practice, but in this case it works.
        """

        for k, v in six.iteritems(kwargs):
            if k.startswith('action_'):
                """ Rename action parameters that have a name overlap with a connection Parameter.
                    Sometimes the Method has an input kwarg that overlaps with a connection kwarg
                    (timeout is the common one)
                    This method will look for a parameter prefixed with 'action_' and replace it
                    in self.kwargs without the prefix.
                    Should be called only after _setup_connection()
                """

                # Strip off the prefix 'action_'
                stripped_key = k[7:]

                # Validate that we aren't about to overwrite a connection parameter
                if stripped_key in self.action_kwargs:
                    self.logger.error(
                        'A connection parameter ({}) was attempted to be overwritten with \
                        an action parameter ({}). Please ensure _parameter_housekeeping() \
                        is only called after _setup_connection()'.format(stripped_key, k))
                    sys.exit(1)

                else:
                    # Create self.action_kwargs['<key>'] with the value of
                    # self.action_kwargs['action_<key>'], and remove
                    # self.action_kwargs['action_<key>']
                    self.action_kwargs[stripped_key] = self.action_kwargs.pop(
                        k)
                    self.logger.debug(
                        'Action Parameter "{}" updated'.format(stripped_key))

            elif k.startswith('_'):
                """ Remove parameters from kwargs that are just for populating other fields
                    Looks for a parameter prefix of a single underscore

                    Because of the strictness of pan-python's methods and kwarg inputs,
                    you cannot pass it erroneous kwargs or it will throw an error.

                    When creating actions you can have parameters that are used to populate
                    other parameters. This is really useful for creating simplified versions
                    of potentially complicated action inputs.

                    Example from xapi.commit.panorama.device_group

                      cmd:
                        description: An XML document used to specify commit arguments (as a string)
                        type: string
                        default: <commit-all>
                                   <shared-policy>
                                     <device-group>
                                       <entry name='{{ _device_group }}'/>
                                      </device-group>
                                    </shared-policy>
                                  </commit-all>
                        immutable: true
                      _device_group:
                        description: The name of the device-group that the commit should \
                                     have changes pushed to
                        type: string
                        required: true

                    Once the initial action is rendered and the parameter 'cmd' is populated,
                    '_device_group' can be thrown away.
                """

                # Parameter is not needed, so throw it away
                self.action_kwargs.pop(k)

        # Nothing really cares about this, but return True so it can be checked
        return True
