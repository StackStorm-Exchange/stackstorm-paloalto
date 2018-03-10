# Palo Alto Networks Pack

This pack uses the Palo Alto Network developed library [pandevice](https://github.com/PaloAltoNetworks/pandevice) to implement a number of functions for interaction with Palo Alto Networks devices.

The actions in this pack are Panorama aware when appropiate. In most cases, you will reference the Panorama as the `firewall` and a desired device group via `device_group`.

Block threats on **Palo Alto Networks (_PAN_)** firewalls. This uses PAN **HTTP server profiles** (webhooks) which are available in PAN-OS version 8+.

## Configuration

Copy the example configuration in **paloalto.yaml.example** to */opt/stackstorm/configs/paloalto.yaml* and edit as required. After making changes, tell ST2 to load them with `sudo st2ctl reload --register-configs`.

Example configuration:

```yaml
---
firewall:
  default:
    host: prodfirewall.corp.lan
    api_username: admin
    api_password: admin
```

You can configure serveral devices (both Firewalls and Panoramas) all under the `firewall` config section. The `default` device will be used whenever the `firewall` parameter is not passed in various actions. You may also use an api key instead of username/password for device authentication using the `api_key` parameter in the config of each device.

In order to obtain *Palo Alto API key*, run the command below. Replace `firewall` with the IP address of firewall, and provide the appropriate username and password:

```shell
curl -kgX GET 'https://firewall/api/?type=keygen&user=admin&password=password'
```

## Actions

### Currently, the following actions listed below are supported:
#### Config objects
Add or update an each of these object types on a Firewall/Panorama (or device group):
- address object - `apply_address_object`
- address group - `apply_address_group`
- service object - `apply_service_object`
- service group - `apply_service_group`
- security rule - `apply_security_rule`

The above objects may also be added and updated in bulk:
- `bulk_apply_address_object`
- `bulk_apply_address_group`
- `bulk_apply_service_object`
- `bulk_apply_service_group`
- `bulk_apply_security_rule`

#### IP/Tag registration
You can dynamically register IP Addresses/tags to the device using the User-ID API.
- `register_ip` and `bulk_register_ip`
- `unregister_ip` and `bulk_unregister_ip`

#### Commits
Issue commits to Firewalls and Panorama (including device groups)
- `commit`

## Example Rule

The pack also includes an example rule which can be used to receive webhooks from a Palo Alto Networks Device that contain bad actors and use the pack actions to block those actors.

The rule name is `block_bad_actors` located in the `rules/` directory. The rule receives webhooks from the firewall and registers the IP in the payload with a defined tag to the firewall for inclusion in a Dynamic Address Group to block traffic from the IP.

Configure a http webhook (http server profile) on the firewall/Panorama following the [PAN-OS 8.0 documentation](https://www.paloaltonetworks.com/documentation/80/pan-os/web-interface-help/device/device-server-profiles-http)

![Snapshot of device webhook configuration - payload format](https://github.com/IrekRomaniuk/paloalto_blockthreats/blob/master/pan-webhook.PNG)

Name of the StackStorm server has to match the certificate imported into the firewall/Panorama for connection. The firewall/Panorama will also need a StackStorm API key. To generate a new key run this command:
 ```
st2 apikey create -k -m '{"used_by": "PAN"}'
 ```
For more information, see this [blog post](https://medium.com/@IrekRomaniuk/stackstorm-pack-for-palo-alto-networks-firewall-a7d8a4ea6655).
