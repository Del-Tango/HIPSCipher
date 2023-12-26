#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Encryption Unit Tests

import pytest
import os
import pysnooper

from tst.conftest import sanitize_line
from hips_cipher import *


#@pysnooper.snoop()
def test_encryption(hc_setup_teardown, encryption_data, conf_json):
    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    with open(conf_json['cleartext_file'], 'w') as fl:
        fl.write(''.join(encryption_data))
    result = encrypt(conf_json['cleartext_file'], **conf_json)
    assert result
    assert os.path.exists(result)

