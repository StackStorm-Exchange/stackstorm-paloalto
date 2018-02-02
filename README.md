# Palo Alto firewall Pack

Block threats on **Palo Alto Networks (_PAN_)** firewalls. This uses PAN **HTTP server profiles** (webhooks) which are available in PAN-OS version 8+.

## Configuration

Copy the example configuration in **paloalto.yaml.example** to */opt/stackstorm/configs/paloalto.yaml* and edit as required. After making changes, tell ST2 to load them with `sudo st2ctl reload --register-configs`.

In order to obtain *Palo Alto API key*, run the command below. Replace `firewall` with the IP address of firewall, and provide the appropriate username and password:

```shell
curl -kgX GET 'https://firewall/api/?type=keygen&user=admin&password=password'
```

Example configuration:

```yaml
---
  api_key: "palo_alto_api_key"
  tag: "st2"
```

## Using the pack

Configure http webhook on PAN following  [PAN-OS 8.0 documentation](https://www.paloaltonetworks.com/documentation/80/pan-os/web-interface-help/device/device-server-profiles-http)

![Snapshot of PAN webhook configuration - payload format](https://github.com/IrekRomaniuk/paloalto_blockthreats/blob/master/pan-webhook.PNG)

Name of _st2 server_ has to match st2 certificate imported to PAN. To get *st2 API key*, run the command below
 ```
st2 apikey create -k -m '{"used_by": "PAN"}'
 ```
See my blog post [here](https://medium.com/@IrekRomaniuk/stackstorm-pack-for-palo-alto-networks-firewall-a7d8a4ea6655).

## Actions

Currently, the following actions listed below are supported:
- register IP to DAG (Dynamic Address Group)

