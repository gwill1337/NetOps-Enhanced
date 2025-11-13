# Configuration Guide - `config.yaml`

This file defines which parts of your network are **critical**, **sensitive**, or **restricted**.  
It is used by both **validation** and **security** tests in Batfish + Pytest setups.

---

## Example

```yaml
critical_nodes:
  - Core1
  - Core2

critical_dests:
  - 192.168.10.0/24
  - 172.16.0.0/16

user_sources:
  - 10.0.0.0/8
  - 172.20.0.0/16

management_hosts:
  - 192.168.10.10/32
```
## Field Reference
### critical_nodes

```yaml
critical_nodes:
  - Core1
  - Core2
```

**Meaning:**   
List of core or essential devices in your topology.   
These are usually routers or switches that form the network backbone.

**Used for:**   
*  Ensuring they are reachable.
*  Checking BGP/OSPF sessions between them.
*  Detecting configuration drift or inactive interfaces.
  
### critical_dests


```yaml
critical_dests:
  - 192.168.10.0/24
  - 172.16.0.0/16
```

**Meaning:**   
Important network segments that must remain reachable (e.g., data centers, servers, databases).

**Used for:**
* Validating connectivity between core nodes and key destinations.
* Detecting broken routing paths or ACLs blocking critical traffic.
  
### user_sources
```yaml
user_sources:
  - 10.0.0.0/8
  - 172.20.0.0/16
```
**Meaning:**   
User or branch office subnets (client networks).   
These represent less-trusted zones in your topology.   

**Used for:**
* Security testing (access restrictions).
* Verifying users cannot reach management or internal resources.
* Checking ACL and routing isolation between user and management zones.

### management_hosts

```yaml
management_hosts:
  - 192.168.10.10/32
  - 192.168.10.11/32
```

**Meaning:**  
Management devices and systems (e.g., NMS, SSH, SNMP, monitoring).   
These are highly sensitive and should be reachable only from trusted networks.

**Used for:**
* Security compliance tests.
* Ensuring ACLs restrict access to management systems.
* Detecting if user zones can access these hosts (misconfiguration).
