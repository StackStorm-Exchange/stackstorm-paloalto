from lib.base import BaseAction
import sys


class Action(BaseAction):
    """ Commands the begin with 'debug' or 'request' are disallowed through the API.
        The official stance from PAN was that they are not supported features at this time.
        While it's reasonable that you wouldn't want someone to be able to turn on a debug
        or execute a request that may criple a firewall, many valid uses cases require
        to issue these kinds of commands.

        Example: 'request restart system' or 'debug software restart management-server'
    """
    def run(self, **kwargs):

        command = kwargs.pop('command', None)

        self._resolve_connection(**kwargs)

        self.netmiko = self.netmiko_client(host=self.hostname,
                                           username=self.username,
                                           password=self.password)

        self.logger.debug(
            'sending command "{}"'.format(command))

        try:
            result = self.netmiko.send_command(command)
        except Exception as e:
            self.logger.error(e)
            sys.exit(1)

        # netmiko returns 2 lines that are generally garbage, so strip them off
        result = '\n'.join(result.split('\n')[2:])

        return result

    def _resolve_connection(self, **kwargs):
        """ works through connection option conflicts
        """

        if 'connection_name' in kwargs and kwargs['connection_name']:
            connection = self.retieve_config_connection(kwargs['connection_name'])

        if 'hostname' in kwargs and kwargs['hostname']:
            self.hostname = kwargs['hostname']
        elif connection and 'hostname' in connection and connection['hostname']:
            self.hostname = connection['hostname']
        else:
            raise ValueError('hostname is required but none found')

        if 'username' in kwargs and kwargs['username']:
            self.username = kwargs['username']
        elif connection and 'api_username' in connection and connection['api_username']:
            self.username = connection['api_username']
        else:
            raise ValueError('username is required but none found')

        if 'password' in kwargs and kwargs['password']:
            self.password = kwargs['password']
        elif connection and 'api_password' in connection and connection['api_password']:
            self.password = connection['api_password']
        else:
            raise ValueError('password is required but none found')

        return True
