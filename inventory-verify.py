import socket
import argparse
import re

class TargetAction (argparse.Action):
    def __call__ (self, parser, namespace, values, option_string=None):

        # now lets create a hosts array from a text file
        try:
            with open(values, 'r') as fh:
                hosts = [
                    s # declares s
                    for line in fh
                    if (s := line.strip()) # gets rid of empty lines 
                    and not s.startswith(("#", "[]")) # skips comments and headers
                    and "ansible_host" in s # keep only if contains ansible_host
                ]
            # for debugging
            #for item in hosts: 
                #print (item)
        except FileNotFoundError:
            print(f"Error: The file {values} was not found.")
            return

        mismatch_dict = {}
        
        # uses socket to do a dns lookup of hosts
        for line in hosts:
            # now ip needs to be gotten with a regex
            
            # vim commands
            # ip = :'<,'>s/.*=\(.*\)/\1/
            # host = :'<,'>s/\(.*\)\s/\1/

            host = re.search(r"(.*)\s", line).group(1).strip()
            inven_ip = re.search(r".*=(.*)", line).group(1).strip()

            try:
                ip = socket.gethostbyname(host)
                # print(f"{host} -> {ip} ", end="") # no newline
                if ip == inven_ip:
                    continue
                    # print ("inventory is correct")
                else:
                    mismatch_dict.update({host : f"inventory address is {inven_ip} but found host at {ip}"})
                    # print ()
            except socket.gaierror:
                mismatch_dict.update({host: f"host not found"})


        for key, value in mismatch_dict.items():
            print (f"{key}: {value}")
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(
                    prog='lookup-hosts',
                    description='given an ansible inventory file will lookup all the ips inventory',
                    epilog='change the world...')

# target positional arg
parser.add_argument('-t', '--target', metavar="FILE", help='reads target for list of hosts', action=TargetAction)

args = parser.parse_args()
