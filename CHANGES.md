# Change Log

## 0.4.0

- Overhaul of pack
- Add a lot more things here :)

## 0.3.3

- Python 3 fixups
- Add explicit support for Python 2 and 3

## 0.3.2
- Version bump to fix tagging issues

## 0.3.1
- Broke out commit-all into its own action (`commit_all`) for Panorama devices
- Fixed the `str()` test in the bulk delete action

## 0.3.0
- Fixed bulk apply actions so that they work when updating existing objects
- Added delete/bulk delete actions. These actions take an object name(s) as input to delete.

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
