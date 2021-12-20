# Change Log

## 1.1.0

- Complete Pack rework (Old actions still present for now, old/new logic is in parallel)
- The following Actions are now deprecated and will be removed in a future release. If you use these please begin migrating your usage to new actions.
  - apply_address_group
  - apply_address_object
  - apply_security_rule
  - apply_service_group
  - apply_service_object
  - bulk_apply_address_groups
  - bulk_apply_address_objects
  - bulk_apply_security_rules
  - bulk_apply_service_groups
  - bulk_apply_service_objects
  - bulk_delete_address_groups
  - bulk_delete_address_objects
  - bulk_delete_security_rules
  - bulk_delete_service_groups
  - bulk_delete_service_objects
  - bulk_register_ip
  - bulk_unregister_ip
  - commit
  - commit_all
  - delete_address_group
  - delete_address_object
  - delete_security_rule
  - delete_service_group
  - delete_service_object
  - get_address_groups
  - get_address_objects
  - get_security_rules
  - get_service_groups
  - get_service_objects
  - register_ip
  - unregister_ip
- New Actions
  - XApi - Used for actions interacting with the Palo Alto XAPI
    - https://docs.paloaltonetworks.com/pan-os/9-0/pan-os-panorama-api/get-started-with-the-pan-os-xml-api
  - LicApi - Used for interacting with the cloud based Licensing API
    - https://docs.paloaltonetworks.com/vm-series/8-1/vm-series-deployment/license-the-vm-series-firewall/licensing-api.html
  - WFApi - Used for interacting with the cloud based Wild Fire API
    - https://docs.paloaltonetworks.com/wildfire/u-v/wildfire-api.html
  - AFApi - Used for interacting with the cloud based AutoFocus API
    - https://docs.paloaltonetworks.com/autofocus/autofocus-api.html
- Shortcut Actions
  - Shortcut actions are a way of leveraging an existing action (like `xapi.set`) in a way that simplifies the input process. Normally you would need fairly detailed xml/xpath data to make an new address group object. A shortcut action allows you to define the xml/xpath structure, and add parameters to the action definition that can be inserted into the xml/xpath at run time. See the readme section under 'Tricks Used' for more details.
  - Example: [xapi.delete.panorama.address.shared](./actions/xapi.delete.panorama.address.shared.yaml)
- Configuration - The config now supports the top level key `connections` for use with new actions.

## 1.0.0

* Drop Python 2.7 support

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
