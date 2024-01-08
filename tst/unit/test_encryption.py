#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Encryption Unit Tests

import pytest
import os
import pysnooper

from hips_cipher import *


#@pysnooper.snoop()
def test_encryption(hc_setup_teardown, encryption_data, conf_json):
    global action_result
    action_result = {
        'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []
    }
    conf_json.update({'running_mode': 'encrypt', 'data_source': 'file'})
    lock_n_load = setup(**conf_json)
    assert lock_n_load
    with open(conf_json['cleartext_file'], 'w') as fl:
        fl.write(''.join(encryption_data))
    check = check_preconditions(**conf_json)
    assert check
    result = encrypt(conf_json['cleartext_file'], **conf_json)
    assert result
    assert os.path.exists(result)
    os.remove(result)
    os.remove(conf_json['cleartext_file'])

