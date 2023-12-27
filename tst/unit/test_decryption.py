#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Decryption Unit Tests

import pytest
import os
import pysnooper

from hips_cipher import *


#@pysnooper.snoop()
def test_decryption(hc_setup_teardown, conf_json):
    conf_json.update({'running_mode': 'decrypt'})
    action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}
    print('[ DEBUG ]: conf_json', conf_json)


    lock_n_load = setup(**conf_json)
    assert lock_n_load
    if os.path.exists(conf_json['cleartext_file']):
        os.remove(conf_json['cleartext_file'])
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    conf_json['image_file'] = crypted_img
    check = check_preconditions(**conf_json)
    assert check
    result = decrypt(**conf_json)
    assert result
    assert os.path.exists(result)

