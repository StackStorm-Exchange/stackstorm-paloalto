# Change Log
## 0.2.1
- Fixed a bug in actions to apply a single object.
- Added actions to get objects from the firewall.

## 0.2.0
Overhauled pack with breaking changes.

Under the hood, the pack now uses [pandevice](https://github.com/PaloAltoNetworks/pandevice). Also added a number of new actions:
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

You may register and unregister IP Address/tags
- `register_ip` and `bulk_register_ip`
- `unregister_ip` and `bulk_unregister_ip`

Issue commits to Firewalls and Panorama (including device groups)
- `commit`

## 0.1.0
- First release
