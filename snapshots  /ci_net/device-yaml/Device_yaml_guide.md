# Guide Yaml for generating configs
## **explanation, template below**
### Interfaces
```yaml
- hostname: device-1                 # <--- Device hostname
  os: cisco                          # <--- Device OS: cisco | juniper | paloalto

  mgmt:                               # <--- Management parameters (common for all vendors)
    ip: 192.168.1.10                  # <--- Management IP address
    mask: 24                          # <--- Management subnet mask prefix
    gateway: 192.168.1.1              # <--- Default gateway for management traffic

  interfaces:                         # <--- List of all interfaces on the device
    - name: uplink                    # <--- Logical interface name (universal)
      physical: GigabitEthernet0/0   # <--- Cisco physical interface name
      unit: ge-0/0/0                 # <--- Juniper interface name
      pa: ethernet1/1                # <--- Palo Alto interface name
      ip: 10.0.0.1                   # <--- Interface IP address
      prefix: 24                     # <--- IP prefix length
      description: "Uplink to core"  # <--- Interface description
      enabled: true                  # <--- true = enabled, false = shutdown

    - name: mgmt-if                   # <--- Second interface example
      physical: GigabitEthernet0/1
      unit: ge-0/0/1
      pa: ethernet1/2
      ip: 10.10.10.1
      prefix: 24
      description: "Management interface"
      enabled: true                # <--- true = enabled, false = shutdown
```
**P.S. The interface field will be taken from the vendor whose OS you enter in the field. Exampe: If you write in foield os: cisco will be taken <u>physical</u> one, see comments on interfaces**

### Routing
```yaml
routing:                             # <--- Routing configuration block
    bgp:                               # <--- BGP configuration (universal)
      local_as: 65001                  # <--- Local AS number
      router_id: 10.0.0.1              # <--- BGP router ID

      neighbors:                       # <--- BGP neighbors list
        - address: 10.0.0.2            # <--- Neighbor IP
          remote_as: 65002             # <--- Peer’s AS
          description: "core uplink"   # <--- Optional neighbor description

        - address: 10.0.0.3
          remote_as: 65003
          description: "backup link"

    static:                             # <--- Static routes
      - network: "0.0.0.0/0"            # <--- Destination prefix
        next_hop: 10.0.0.254            # <--- Next-hop IP

      - network: "192.168.50.0/24"
        next_hop: 10.10.10.254
```
### Security
```yaml
security:                             # <--- Security rules (generic)
    acls:                                # <--- Access lists (Cisco/Juniper equivalent)
      - name: mgmt-access                # <--- ACL name
        rules:
          - action: permit               # <--- permit/deny
            protocol: tcp                # <--- tcp/udp/ip
            src: 10.10.0.0/16            # <--- Source network
            dst: 10.0.0.1                # <--- Destination IP
            dst_port: 22                 # <--- Destination port

          - action: deny
            protocol: ip
            src: any
            dst: any

    policies:                            # <--- Palo Alto style policies (optional for others)
      - name: allow-web                  # <--- Security policy name
        from: trust                      # <--- Source zone
        to: untrust                      # <--- Destination zone
        src: ["10.10.0.0/24"]            # <--- Source addresses list
        dst: ["any"]                     # <--- Destination addresses
        apps: ["web-browsing"]           # <--- Applications
        action: allow      
```

### Other
```yaml
default_gateway: 10.0.0.254           #<--- Default route next-hop
```

### Entire config yaml
```yaml
- hostname: device-1                 # <--- Device hostname
  os: cisco                          # <--- Device OS: cisco | juniper | paloalto

  mgmt:                               # <--- Management parameters (common for all vendors)
    ip: 192.168.1.10                  # <--- Management IP address
    mask: 24                          # <--- Management subnet mask prefix
    gateway: 192.168.1.1              # <--- Default gateway for management traffic

  interfaces:                         # <--- List of all interfaces on the device
    - name: uplink                    # <--- Logical interface name (universal)
      physical: GigabitEthernet0/0   # <--- Cisco physical interface name
      unit: ge-0/0/0                 # <--- Juniper interface name
      pa: ethernet1/1                # <--- Palo Alto interface name
      ip: 10.0.0.1                   # <--- Interface IP address
      prefix: 24                     # <--- IP prefix length
      description: "Uplink to core"  # <--- Interface description
      enabled: true                  # <--- true = enabled, false = shutdown

    - name: mgmt-if                   # <--- Second interface example
      physical: GigabitEthernet0/1
      unit: ge-0/0/1
      pa: ethernet1/2
      ip: 10.10.10.1
      prefix: 24
      description: "Management interface"
      enabled: true

  routing:                             # <--- Routing configuration block
    bgp:                               # <--- BGP configuration (universal)
      local_as: 65001                  # <--- Local AS number
      router_id: 10.0.0.1              # <--- BGP router ID

      neighbors:                       # <--- BGP neighbors list
        - address: 10.0.0.2            # <--- Neighbor IP
          remote_as: 65002             # <--- Peer’s AS
          description: "core uplink"   # <--- Optional neighbor description

        - address: 10.0.0.3
          remote_as: 65003
          description: "backup link"

    static:                             # <--- Static routes
      - network: "0.0.0.0/0"            # <--- Destination prefix
        next_hop: 10.0.0.254            # <--- Next-hop IP

      - network: "192.168.50.0/24"
        next_hop: 10.10.10.254

  security:                             # <--- Security rules (generic)
    acls:                                # <--- Access lists (Cisco/Juniper equivalent)
      - name: mgmt-access                # <--- ACL name
        rules:
          - action: permit               # <--- permit/deny
            protocol: tcp                # <--- tcp/udp/ip
            src: 10.10.0.0/16            # <--- Source network
            dst: 10.0.0.1                # <--- Destination IP
            dst_port: 22                 # <--- Destination port

          - action: deny
            protocol: ip
            src: any
            dst: any

    policies:                            # <--- Palo Alto style policies (optional for others)
      - name: allow-web                  # <--- Security policy name
        from: trust                      # <--- Source zone
        to: untrust                      # <--- Destination zone
        src: ["10.10.0.0/24"]            # <--- Source addresses list
        dst: ["any"]                     # <--- Destination addresses
        apps: ["web-browsing"]           # <--- Applications
        action: allow                    # <--- allow / deny

```



## Template
```yaml
- hostname:
  os:

  mgmt:
    ip:
    mask:
    gateway:

  interfaces:
    - name:
      physical:
      unit:
      pa:
      ip:
      prefix:
      description:
      enabled:

  routing:
    bgp:
      local_as:
      router_id:
      neighbors:
        - address:
          remote_as:
          description:

    static:
      - network:
        next_hop:

  security:
    acls:
      - name:
        rules:
          - action:
            protocol:
            src:
            dst:
            dst_port:

    policies:
      - name:
        from:
        to:
        src:
        dst:
        apps:
        action:

```
