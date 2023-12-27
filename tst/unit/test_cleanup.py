#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Cleanup Unit Tests

import pytest
import os
import pysnooper

from tst.conftest import shell_cmd
from hips_cipher import *


@pysnooper.snoop()
def test_cleanup(hc_setup_teardown, hc_encryption_cmd, encryption_data, conf_json):
    global action_result
    action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}
    conf_json.update({'running_mode': 'cleanup', 'report': True})
    create_cleartext = write2file(
        *encryption_data, file_path=conf_json['cleartext_file'], mode='w'
    )
    assert create_cleartext
    out, err, exit = shell_cmd(' '.join(hc_encryption_cmd))
    assert exit == 0
    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    result = cleanup(**conf_json)
    assert result
    for label in conf_json['cleanup']:
        assert not os.path.exists(conf_json[label])

@pysnooper.snoop()
def test_full_cleanup(hc_setup_teardown, hc_encryption_cmd, encryption_data, conf_json):
    conf_json.update({'running_mode': 'cleanup', 'report': True})
    create_cleartext = write2file(
        *encryption_data, file_path=conf_json['cleartext_file'], mode='w'
    )
    assert create_cleartext
    out, err, exit = shell_cmd(' '.join(hc_encryption_cmd))
    assert exit == 0
    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    result = cleanup(full=True, **conf_json)
    assert result
    for label in conf_json['full_cleanup']:
        assert not os.path.exists(conf_json[label])
