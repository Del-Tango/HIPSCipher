#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# EXIF Manipulation Integration Tests

import pytest
import json
import os
import shutil
import pysnooper

from tst.conftest import shell_cmd
from hips_cipher import write2file, file2list


#@pysnooper.snoop()
def test_exif_dump(hc_setup_teardown, hc_dump_exif_cmd, conf_json):
    cmd = hc_dump_exif_cmd + [
        '--image-file', conf_json['image_file'],
    ]
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0

#@pysnooper.snoop()
def test_exif_write(hc_setup_teardown, hc_write_exif_cmd, conf_json):
    cmd = hc_write_exif_cmd + [
        '--image-file', conf_json['image_file'],
        '--exif-tag', str(conf_json['exif_tag']),
        '--exif-data', conf_json['exif_data'],
    ]
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    assert os.path.exists(crypted_img)

#@pysnooper.snoop()
def test_exif_read(hc_setup_teardown, hc_read_exif_cmd, conf_json):
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    assert os.path.exists(crypted_img)
    cmd = hc_read_exif_cmd + [
        '--image-file', crypted_img,
        '--exif-tag', str(conf_json['exif_tag']),
    ]
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0

#@pysnooper.snoop()
def test_exif_clean(hc_setup_teardown, hc_clean_exif_cmd, conf_json):
    img_dir = os.path.dirname(conf_json['image_file'])
    img_fl = os.path.basename(conf_json['image_file'])
    crypted_img = img_dir + '/hips.' + img_fl
    crypted_copy = img_dir + '/hips.hips.' + img_fl
    assert os.path.exists(crypted_img)
    shutil.copy2(crypted_img, crypted_copy)
    cmd = hc_clean_exif_cmd + [
        '--image-file', crypted_copy,
    ]
    out, err, exit = shell_cmd(' '.join(cmd))
    assert exit == 0

