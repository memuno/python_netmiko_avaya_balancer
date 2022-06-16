from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint

# Test commmand Cisco Oficina

command = 'clist policy\n'

# Connect to Terminal ssh Avaya
net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="10.85.123.110",
    username="mgomez",
    password=getpass(),
)

print(net_connect.find_prompt())

output = net_connect.send_command(
    command_string='sat',
    expect_string=r"Terminal",
    strip_prompt=False,
    strip_command=False

)

output += net_connect.send_command(
    command_string='ossit\n',
    expect_string=r"t\n",
    strip_prompt=False,
    strip_command=False

)

output += net_connect.send_command(
    command_string= command,
    expect_string=r"",
    strip_prompt=False,
    strip_command=False

)

output += net_connect.send_command(
    command_string= 't\n',
    expect_string=r"more",
    strip_prompt=False,
    strip_command=False

)
print(output)
net_connect.disconnect()

