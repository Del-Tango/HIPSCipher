#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Decryption Integration Tests

import pytest
import json
import os
import pysnooper

from tst.conftest import shell_cmd
from hips_cipher import write2file, file2list, cleanup


#@pysnooper.snoop()
def test_file_base_decryption_from_cli(hc_setup_teardown, hc_decryption_cmd,
        hc_encryption_cmd, encryption_data, conf_json):
    conf_json.update({'running_mode': 'decrypt', 'report': False})

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
    conf_json['image_file'] = crypted_img
    cmd = hc_decryption_cmd + [
        '--image-file', conf_json['image_file'],
        '--key-code', conf_json['keycode'],
    ]
    if os.path.exists(conf_json['cleartext_file']):
        os.remove(conf_json['cleartext_file'])
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    cleartext_content = file2list(conf_json['cleartext_file'])
    assert cleartext_content

#@pysnooper.snoop()
def test_file_base_decryption_from_cli_silently(hc_setup_teardown, hc_decryption_cmd, conf_json):
    conf_json.update({'running_mode': 'decrypt', 'report': False})
    if os.path.exists(conf_json['cleartext_file']):
        os.remove(conf_json['cleartext_file'])
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    conf_json['image_file'] = crypted_img
    cmd = hc_decryption_cmd + [
        '--image-file', conf_json['image_file'],
        '--key-code', conf_json['keycode'],
        '--silent'
    ]
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    cleartext_content = file2list(conf_json['cleartext_file'])
    assert cleartext_content

#@pysnooper.snoop()
def test_file_base_decryption_from_cli_reported(hc_setup_teardown, hc_decryption_cmd, conf_json):
    conf_json.update({'running_mode': 'decrypt', 'report': True})
    if os.path.exists(conf_json['cleartext_file']):
        os.remove(conf_json['cleartext_file'])
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    conf_json['image_file'] = crypted_img
    cmd = hc_decryption_cmd + [
        '--image-file', conf_json['image_file'],
        '--key-code', conf_json['keycode'],
        '--silent'
    ]
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    assert os.path.exists(conf_json['report_file'])
    cleartext_content = file2list(conf_json['cleartext_file'])
    assert cleartext_content
    report_content = {}
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
def test_file_base_decryption_from_config(hc_setup_teardown, hc_konfig_cmd, conf_json): #decryption_data,
    conf_json.update({'running_mode': 'decrypt', 'report': True})
    if os.path.exists(conf_json['cleartext_file']):
        os.remove(conf_json['cleartext_file'])
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    conf_json['image_file'] = crypted_img
    write2file(
        json.dumps(conf_json, indent=4), file_path=conf_json['config_file'], mode='w'
    )
    out, err, exit = shell_cmd(' '.join(hc_konfig_cmd))
    assert exit == 0
    cleartext_content = file2list(conf_json['cleartext_file'])
    assert cleartext_content

