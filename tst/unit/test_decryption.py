#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Decryption Unit Tests

import pytest
import os
import pysnooper

from hips_cipher import *


#@pysnooper.snoop()
def test_decryption(hc_setup_teardown, encryption_data, conf_json):
    global action_result
    conf_json.update({'running_mode': 'decrypt'})
    action_result = {
        'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []
    }
    lock_n_load = setup(**conf_json)
    assert lock_n_load
    if os.path.exists(conf_json['cleartext_file']):
        os.remove(conf_json['cleartext_file'])
    check = check_preconditions(**conf_json)
    assert check
    conf_json.update({
        'running_mode': 'encrypt',
        'data_source': 'file',
        'in_line': False
    })
    with open(conf_json['cleartext_file'], 'w') as fl:
        fl.write(''.join(encryption_data))
    crypted_img = encrypt(conf_json['cleartext_file'], **conf_json)
    assert crypted_img
    conf_json.update({
        'running_mode': 'decrypt',
        'image_file': crypted_img,
    })
    os.remove(conf_json['cleartext_file'])
    result = decrypt(**conf_json)
    assert result
    assert os.path.exists(result)
    assert os.path.exists(conf_json['cleartext_file'])
    os.remove(crypted_img)

