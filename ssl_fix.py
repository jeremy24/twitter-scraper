
# this file is to fix some issues
#   when making requests ubuntu

import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()
