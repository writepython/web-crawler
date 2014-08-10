import os, sys, platform

def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

print("""Python Version: %s
Platform -> Distribution: %s
Platform -> Linux Distribution: %s
Platform -> System: %s
Platform -> Machine: %s
Platform -> Platform: %s
Platform -> Uname: %s
Platform -> Version: %s
Platform -> Mac Version: %s
SYS -> Platform: %s
OS -> Name: %s
""" % (
sys.version.split('\n'),
str(platform.dist()),
linux_distribution(),
platform.system(),
platform.machine(),
platform.platform(),
platform.uname(),
platform.version(),
platform.mac_ver(),
sys.platform,
os.name
))
