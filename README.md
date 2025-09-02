# Ansible-Inventory-Verifier
Ensure that an ansible inventory lists accurate host information. 

## Usage
`python inventory-verifier.py -t inventory`

## Example Output
```
example-host-1: inventory address is 10.32.6.1 but found host at 10.24.6.100
example-host-2: host not found
example-host-3: host not found
example-host-4: host not found
example-host-5: host not found
example-host-6: host not found
```
