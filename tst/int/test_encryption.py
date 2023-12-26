#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Encryption Integration Tests

import pytest
import json
import os
import pysnooper

from tst.conftest import shell_cmd
from hips_cipher import write2file, file2list


#@pysnooper.snoop()
def test_file_base_encryption_from_cli(hc_setup_teardown, hc_encryption_cmd,
                                       encryption_data, conf_json):
    conf_json.update({'running_mode': 'encrypt', 'report': False})
    write2file(
        json.dumps(conf_json, indent=4), file_path=conf_json['config_file'], mode='w'
    )
    cmd = hc_encryption_cmd + [
        '--image-file', conf_json['image_file'],
        '--cleartext-file', conf_json['cleartext_file'],
        '--key-code', conf_json['keycode'],
    ]
    write2file(
        *encryption_data, file_path=conf_json['cleartext_file'], mode='w'
    )
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    assert os.path.exists(crypted_img)

#@pysnooper.snoop()
def test_file_base_encryption_from_cli_silently(hc_setup_teardown, hc_encryption_cmd,
                                                encryption_data, conf_json):
    conf_json.update({'running_mode': 'encrypt', 'report': False})
    cmd = hc_encryption_cmd + [
        '--image-file', conf_json['image_file'],
        '--cleartext-file', conf_json['cleartext_file'],
        '--key-code', conf_json['keycode'],
        '--silent',
    ]
    write2file(
        *encryption_data, file_path=conf_json['cleartext_file'], mode='w'
    )
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    assert os.path.exists(crypted_img)

#@pysnooper.snoop()
def test_file_base_encryption_from_cli_reported(hc_setup_teardown, hc_encryption_cmd,
                                                encryption_data, conf_json):
    conf_json.update({'running_mode': 'encrypt', 'report': True})
    cmd = hc_encryption_cmd + [
        '--image-file', conf_json['image_file'],
        '--cleartext-file', conf_json['cleartext_file'],
        '--key-code', conf_json['keycode'],
        '--silent'
    ]
    write2file(
        *encryption_data, file_path=conf_json['cleartext_file'], mode='w'
    )
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    assert os.path.exists(conf_json['report_file'])
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    assert os.path.exists(crypted_img)
    with open(conf_json['report_file'], 'r') as fl:
        report_content = json.load(fl)
    assert report_content['input']
    assert isinstance(report_content['input'], list)
    assert report_content['output']
    assert isinstance(report_content['output'], list)
    assert isinstance(report_content['msg'], str)
    assert isinstance(report_content['exit'], int)
    assert report_content['exit'] == 0

#@pysnooper.snoop()
def test_file_base_encryption_from_config(hc_setup_teardown, hc_konfig_cmd,
                                        encryption_data, conf_json):
    conf_json.update({'running_mode': 'encrypt'})
    write2file(
        json.dumps(conf_json, indent=4), file_path=conf_json['config_file'], mode='w'
    )
    write2file(
        *encryption_data, file_path=conf_json['cleartext_file'], mode='w'
    )
    out, err, exit = shell_cmd(' '.join(hc_konfig_cmd))
    assert exit == 0
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    assert os.path.exists(crypted_img)
