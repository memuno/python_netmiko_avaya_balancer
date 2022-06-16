# test library netmiko
from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint

# Simple Example

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="cisco1.lasthop.io",
    username="pyclass",
    password=getpass(),
)

print(net_connect.find_prompt())
net_connect.disconnect()

# Connect using dictionary

cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
}

net_connect = ConnectHandler(**cisco1)
print(net_connect.find_prompt())
net_connect.disconnect()

# Dictionary with a context manager

cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
}

# Will automatically 'disconnect()'
with ConnectHandler(**cisco1) as net_connect:
    print(net_connect.find_prompt())


# Using Genie-- Ouput command to json

device = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass()
}

with ConnectHandler(**device) as net_connect:
    output = net_connect.send_command("show ip interface brief", use_genie=True)

print()
pprint(output) # json
print()

# Handling commands that prompt (timing)

cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
}

command = "del flash:/test3.txt"
net_connect = ConnectHandler(**cisco1)

# CLI Interaction is as follows:
# cisco1#delete flash:/testb.txt
# Delete filename [testb.txt]? 
# Delete flash:/testb.txt? [confirm]y

# Use 'send_command_timing' which is entirely delay based.
# strip_prompt=False and strip_command=False make the output
# easier to read in this context.
output = net_connect.send_command_timing(
    command_string=command,
    strip_prompt=False,
    strip_command=False
)
if "Delete filename" in output:
    output += net_connect.send_command_timing(
        command_string="\n",
        strip_prompt=False,
        strip_command=False
    )
if "confirm" in output:
    output += net_connect.send_command_timing(
        command_string="y",
        strip_prompt=False,
        strip_command=False
    )
net_connect.disconnect()

print()
print(output)
print()

'''
Output from the above execution:
Password: 

del flash:/test3.txt
Delete filename [test3.txt]? 
Delete flash:/test3.txt? [confirm]y
cisco1#
cisco1#

'''


# Handling commands that prompt (expect_string)

cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
}

command = "del flash:/test4.txt"
net_connect = ConnectHandler(**cisco1)

# CLI Interaction is as follows:
# cisco1#delete flash:/testb.txt
# Delete filename [testb.txt]? 
# Delete flash:/testb.txt? [confirm]y

# Use 'send_command' and the 'expect_string' argument (note, expect_string uses 
# RegEx patterns). Netmiko will move-on to the next command when the
# 'expect_string' is detected.

# strip_prompt=False and strip_command=False make the output
# easier to read in this context.
output = net_connect.send_command(
    command_string=command,
    expect_string=r"Delete filename",
    strip_prompt=False,
    strip_command=False
)
output += net_connect.send_command(
    command_string="\n",
    expect_string=r"confirm",
    strip_prompt=False,
    strip_command=False
)
output += net_connect.send_command(
    command_string="y",
    expect_string=r"#",
    strip_prompt=False,
    strip_command=False
)
net_connect.disconnect()

print()
print(output)
print()

'''
Output from the above execution:
$ python send_command_prompting_expect.py 
Password: 

del flash:/test4.txt
Delete filename [test4.txt]? 
Delete flash:/test4.txt? [confirm]y
cisco1#

'''

# Configuration changes--many commands in list
#!/usr/bin/env python

device = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
}

commands = ["logging buffered 100000"]
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_config_set(commands)
    output += net_connect.save_config()

print()
print(output)
print()

'''
Netmiko will automatically enter and exit config mode.
Output from the above execution:
$ python config_change.py 
Password: 

configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
cisco1(config)#logging buffered 100000
cisco1(config)#end
cisco1#write mem
Building configuration...
[OK]
cisco1#

'''

# Configuration changes from a file
#!/usr/bin/env python

device1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
}

# File in same directory as script that contains
#
# $ cat config_changes.txt 
# --------------
# logging buffered 100000
# no logging console

cfg_file = "config_changes.txt"
with ConnectHandler(**device1) as net_connect:
    output = net_connect.send_config_from_file(cfg_file)
    output += net_connect.save_config()

print()
print(output)
print()
'''
Netmiko will automatically enter and exit config mode.
Output from the above execution:
$ python config_change_file.py 
Password: 

configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
cisco1(config)#logging buffered 100000
cisco1(config)#no logging console
cisco1(config)#end
cisco1#write mem
Building configuration...
[OK]
cisco1#
'''

# SSH keys


key_file = "~/.ssh/test_rsa"
cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "testuser",
    "use_keys": True,
    "key_file": key_file,
}

with ConnectHandler(**cisco1) as net_connect:
    output = net_connect.send_command("show ip arp")

print(f"\n{output}\n")

# SSH Config File
#!/usr/bin/env python


cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
    "ssh_config_file": "~/.ssh/ssh_config",
}

with ConnectHandler(**cisco1) as net_connect:
    output = net_connect.send_command("show users")

print(output)
'''
Contents of 'ssh_config' file
host jumphost
  IdentitiesOnly yes
  IdentityFile ~/.ssh/test_rsa
  User gituser
  HostName pynetqa.lasthop.io

host * !jumphost
  User pyclass
  # Force usage of this SSH config file
  ProxyCommand ssh -F ~/.ssh/ssh_config -W %h:%p jumphost
  # Alternate solution using netcat
  #ProxyCommand ssh -F ./ssh_config jumphost nc %h %p
Script execution
# 3.82.44.123 is the IP address of the 'jumphost'
$ python conn_ssh_proxy.py 
Password: 

Line       User       Host(s)              Idle       Location
*  8 vty 0     pyclass    idle                 00:00:00 3.82.44.123

  Interface    User               Mode         Idle     Peer Address

'''

# Session log
#!/usr/bin/env python

cisco1 = {
    "device_type": "cisco_ios",
    "host": "cisco1.lasthop.io",
    "username": "pyclass",
    "password": getpass(),
    # File name to save the 'session_log' to
    "session_log": "output.txt"
}

# Show command that we execute
command = "show ip int brief"
with ConnectHandler(**cisco1) as net_connect:
    output = net_connect.send_command(command)

'''
Contents of 'output.txt' after execution
$ cat output.txt 

cisco1#
cisco1#terminal length 0
cisco1#terminal width 511
cisco1#
cisco1#show ip int brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0              unassigned      YES unset  down                  down    
FastEthernet1              unassigned      YES unset  down                  down    
FastEthernet2              unassigned      YES unset  down                  down    
FastEthernet3              unassigned      YES unset  down                  down    
FastEthernet4              10.220.88.20    YES NVRAM  up                    up      
Vlan1                      unassigned      YES unset  down                  down    
cisco1#
cisco1#exit

'''

