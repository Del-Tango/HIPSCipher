#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# Pytest Config

import pytest
import os
import json

from subprocess import Popen, PIPE
from hips_cipher import load_config, shell_cmd

CURRENT_DIR = os.getcwd()
PYTHON3 = './.venv/bin/python3'

CONFIG = {
    'config_file': '%s/conf/hips_cipher.conf.json' % CURRENT_DIR,
    'current_dir': CURRENT_DIR,
    'batch_dir': '%s/batch' % CURRENT_DIR,
    'tmp_file': '%s/hc_tmp.txt' % CURRENT_DIR,
    'report_file': '%s/hc_report.dump' % CURRENT_DIR,
    'image_file': '%s/dta/Regards.jpg' % CURRENT_DIR,
    'cleartext_file': '%s/hc_clear.txt' % CURRENT_DIR,
    'running_mode': 'encrypt',                                                  # <decrypt|encrypt|write-exif|read-exif|dump-exif|clean-exif>
    'data_source': 'terminal',                                                  # <file|terminal>
    'exif_data': '#!/',
    'exif_tag': 37510,
    'keycode': 'HIPS',                                                          # Encryption password
    'cleanup': ['tmp_file'],                                                    # CONFIG keys containing file paths
    'full_cleanup': [
        'tmp_file', 'cleartext_file', 'report_file'
    ],
    'in_place': True,
    'batch': False,
    'report': True,
    'silent': False,
}

# DATA

@pytest.fixture
def encryption_data():
    return ['FirstLine\n', 'LastLine\n']

@pytest.fixture
def conf_json():
    return CONFIG.copy()

# GENERAL

def sanitize_line(line_data):
    return line_data.rstrip('\n').rstrip(',')

# COMMANDS

@pytest.fixture
def hc_dump_exif_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'dump-exif']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'dump-exif']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_write_exif_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'write-exif']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'write-exif']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_read_exif_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'read-exif']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'read-exif']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_clean_exif_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'clean-exif']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'clean-exif']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_encryption_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'encrypt']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'encrypt']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_decryption_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'decrypt']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'decrypt']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_cleanup_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--action', 'cleanup']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-a', 'cleanup']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_help_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--help']
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-h']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_util_help_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = ['hipscipher', '--help']
    elif context['arg'].lower() == 'short':
        cmd = ['hipscipher', '-h']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def hc_konfig_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = [PYTHON3, './hips_cipher.py', '--konfig-file', CONFIG['config_file']]
    elif context['arg'].lower() == 'short':
        cmd = [PYTHON3, './hips_cipher.py', '-K',  CONFIG['config_file']]
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def bw_build_cmd(*args, **context):
    cmd = ['./build.sh', 'BUILD']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def bw_install_cmd(*args, **context):
    cmd = ['./build.sh', 'INSTALL']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def bw_cleanup_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = ['./build.sh', '--cleanup', '-y']
    elif context['arg'].lower() == 'short':
        cmd = ['./build.sh', '-c', '-y']
    if args:
        cmd = cmd + list(args)
    return cmd

@pytest.fixture
def bw_setup_cmd(*args, **context):
    if not context.get('arg') or context['arg'].lower() == 'long':
        cmd = ['./build.sh', '--setup']
    elif context['arg'].lower() == 'short':
        cmd = ['./build.sh', '-s']
    if args:
        cmd = cmd + list(args)
    return cmd

# SETUP/TEARDOWN

@pytest.fixture
def hc_setup_teardown(bw_setup_cmd, bw_build_cmd, bw_install_cmd, hc_cleanup_cmd):
    out, err, exit = shell_cmd(' '.join(bw_setup_cmd))
    out, err, exit = shell_cmd(' '.join(bw_build_cmd))
    out, err, exit = shell_cmd(' '.join(bw_install_cmd))
    yield exit
    out, err, exit = shell_cmd(' '.join(hc_cleanup_cmd))

@pytest.fixture
def bw_setup_teardown(bw_setup_cmd, bw_cleanup_cmd):
    out, err, exit = shell_cmd(' '.join(bw_setup_cmd))
    yield exit
    out, err, exit = shell_cmd(' '.join(bw_cleanup_cmd))

# CODE DUMP

