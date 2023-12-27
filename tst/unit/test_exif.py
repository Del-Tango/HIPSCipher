#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# EXIF Manipulation Unit Tests

import pytest
import os
import pysnooper

from hips_cipher import *


#@pysnooper.snoop()
def test_exif_dump(hc_setup_teardown, conf_json):
    global action_result
    action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}
    conf_json.update({'running_mode': 'dump-exif'})

    print('[ DEBUG ]: conf_json', conf_json)

    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    result = dump_exif(**conf_json)
    assert result

#@pysnooper.snoop()
def test_exif_write(hc_setup_teardown, conf_json):
    global action_result
    action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}
    conf_json.update({'running_mode': 'write-exif'})
    print('[ DEBUG ]: conf_json', conf_json)


    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    result = write_exif(**conf_json)
    assert result

#@pysnooper.snoop()
def test_exif_read(hc_setup_teardown, conf_json):
    global action_result
    action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}
    conf_json.update({'running_mode': 'write-exif'})
    print('[ DEBUG ]: conf_json', conf_json)


    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    result = write_exif(**conf_json)
    assert result

    conf_json.update({'running_mode': 'read-exif'})
    print('[ DEBUG ]: conf_json', conf_json)


#   lock_n_load = setup(**conf_json)
#   assert lock_n_load
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    conf_json['image_file'] = crypted_img
    check = check_preconditions(**conf_json)
    assert check
    result = read_exif(**conf_json)
    assert result

@pysnooper.snoop()
def test_exif_clean(hc_setup_teardown, conf_json):
    global action_result
    action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}
    conf_json.update({'running_mode': 'clean-exif'})
    print('[ DEBUG ]: conf_json', conf_json)


    lock_n_load = setup(**conf_json)
    assert lock_n_load
    check = check_preconditions(**conf_json)
    assert check
    result = clean_exif(**conf_json)
    assert result

