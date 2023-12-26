#!/usr/bin/python3
#
# Excellent Regards, the Alveare Solutions #!/Society -x
#
# HIPS Cipher Enryptor/Decryptor

import optparse
import os
import json
import pysnooper
import piexif

from typing import List
from subprocess import Popen, PIPE
from PIL import Image, ExifTags

SCRIPT_NAME = 'HIPSCipher'
VERSION = '1.0'
VERSION_NAME = 'Portal'
CURRENT_DIR = os.getcwd()

CONFIG = {
    'config_file': '',
    'current_dir': CURRENT_DIR,
    'batch_dir': '%s/batch' % CURRENT_DIR,
    'tmp_file': '%s/hc_tmp.txt' % CURRENT_DIR,
    'report_file': '%s/hc_report.dump' % CURRENT_DIR,
    'image_file': '%s/dta/Regards.jpg' % CURRENT_DIR,
    'cleartext_file': '%s/hc_cleartext.txt' % CURRENT_DIR,
    'running_mode': 'encrypt',                                                  # <decrypt|encrypt|write-exif|read-exif|dump-exif|clean-exif>
    'data_source': 'terminal',                                                  # <file|terminal>
    'exif_data': '#!/',
    'exif_tag': piexif.ExifIFD.UserComment,
    'keycode': 'HIPS',                                                          # Encryption password
    'cleanup': ['tmp_file'],                                                    # CONFIG keys containing file paths
    'full_cleanup': [
        'tmp_file', 'cleartext_file'
    ],
    'in_place': True,
    'batch': False,
    'report': True,
    'silent': False,
}
action_result = {'input': [], 'output': [], 'msg': '', 'exit': 0, 'errors': []}

# FETCHERS

def fetch_running_mode_from_user(prompt: str = 'Action') -> str:
    global CONFIG
    stdout_msg('Specify action or (.back)...', info=True)
    if CONFIG.get('running_mode'):
        prompt = prompt + '[' + CONFIG['running_mode'] + ']> '
        print(
            '[ INFO ]: Leave blank to keep current '\
            '(%s)' % CONFIG['running_mode']
        )
    stdout_msg(
        '1) Encrypt cleartext\n2) Decrypt ciphertext\n3) Dump all EXIF tags\n' + \
        '4) Read EXIF tag\n5) Write EXIF tag\n6) Disk Cleanup\n' + \
        '7) Clear all EXIF tags'
    )
    selection_map = {
        '1': 'encrypt', '2': 'decrypt', '3': 'dump-exif', '4': 'read-exif',
        '5': 'write-exif', '6': 'cleanup', '7': 'clean-exif'
    }
    while True:
        selection = input(prompt)
        if not selection:
            if not CONFIG.get('running_mode'):
                continue
            selection = [k for k, v in selection_map.items() \
                if v == CONFIG.get('running_mode')][0]
        if selection == '.back':
            return
        if selection not in ('1', '2', '3', '4', '5', '6', '7'):
            print('[ ERROR ]: Invalid selection (%s)' % selection)
        CONFIG['running_mode'] = selection_map[selection]
        break
    print()
    return selection_map[selection]

def fetch_data_from_user(prompt='Data'):
    stdout_msg(
        'Specify input data for action '\
        '(%s) or (.back)...' % CONFIG.get('running_mode', ''), info=True
    )
    if CONFIG.get('running_mode') in (
            'encrypt', 'decrypt', 'cleanup', 'dump-exif', 'read-exif',
            'write-exif', 'clean-exif'
        ):
        prompt = prompt + '[' + CONFIG['running_mode'] + ']'
    while True:
        data = input(prompt + '> ')
        if not data:
            continue
        if data == '.back':
            return
        break
    print()
    return data

#@pysnooper.snoop()
def fetch_exif_tag_from_user(prompt='ExifTag'):
    global CONFIG
    stdout_msg(
        'Specify EXIF tag ID or (.back)...', info=True,
        silence=CONFIG.get('silent')
    )
    if CONFIG.get('exif_tag'):
        prompt = prompt + '[' + str(CONFIG['exif_tag']) + ']> '
        stdout_msg(
            'Leave blank to keep current '\
            '(%s)' % CONFIG['exif_tag'], info=True, silence=CONFIG.get('silent')
        )
    while True:
        tag_id = input(prompt)
        if not tag_id:
            if not CONFIG.get('exif_tag'):
                continue
            tag_id = CONFIG.get('exif_tag')
        if tag_id == '.back':
            return
        try:
            tag_id = int(tag_id)
        except Exception as e:
            stdout_msg(
                'EXIF tag must be a number, not (%s)' % (tag_id), warn=True,
                silence=CONFIG.get('silent')
            )
            continue
        CONFIG.update({'exif_tag': tag_id})
        break
    print()
    return tag_id

def fetch_image_file_path_from_user(prompt='IMGPath'):
    global CONFIG
    stdout_msg(
        'Specify image file path or (.back)...', info=True,
        silence=CONFIG.get('silent')
    )
    if CONFIG.get('image_file'):
        prompt = prompt + '[' + os.path.basename(CONFIG['image_file']) + ']> '
        stdout_msg(
            'Leave blank to keep current '\
            '(%s)' % CONFIG['image_file'], info=True, silence=CONFIG.get('silent')
        )
    while True:
        img_path = input(prompt)
        if not img_path:
            if not CONFIG.get('image_file'):
                continue
            img_path = CONFIG.get('image_file')
        if img_path == '.back':
            return
        CONFIG.update({'image_file': img_path})
        break
    print()
    return img_path

def fetch_replay_confirmation_from_user(prompt='Replay'):
    stdout_msg(
        '[ Q/A ]: Do you want to go again?', silence=CONFIG.get('silent')
    )
    while True:
        answer = input(prompt + '[Y/N]> ')
        if not answer:
            continue
        if answer.lower() not in ('y', 'n', 'yes', 'no', 'yeah', 'nah'):
            print(); stdout_msg(
                'Invalid answer (%s)\n' % answer, err=True,
                silence=CONFIG.get('silent')
            )
            continue
        break
    print()
    return True if answer in ('y', 'yes', 'yeah') else False

def fetch_keycode_from_user(prompt='KeyCode'):
    global CONFIG
    stdout_msg(
        'Specify encryption keycode sequence or (.back)...', info=True,
        silence=CONFIG.get('silent')
    )
    if CONFIG.get('keycode'):
        prompt = prompt + '[' + CONFIG['keycode'] + ']> '
        stdout_msg(
            'Leave blank to keep current '\
            '(%s)' % CONFIG['keycode'], info=True, silence=CONFIG.get('silent')
        )
    while True:
        code = input(prompt)
        if not code:
            if not CONFIG.get('keycode'):
                continue
            code = CONFIG.get('keycode')
        if code == '.back':
            return
        CONFIG.update({'keycode': code})
        break
    print()
    return code

# CHECKERS

#@pysnooper.snoop()
def check_preconditions(**conf):
    errors = []
    file_paths = ['cleartext_file', 'image_file']
    requirements = ['running_mode', 'data_source']
    for fl in file_paths + requirements:
        if not conf.get(fl):
            errors.append('Attribute (%s) not set' % fl)
    if conf.get('running_mode', '').lower() in ('encrypt', 'decrypt') \
            and conf.get('data_source') != 'terminal':
        if not os.path.exists(conf.get('cleartext_file')):
            errors.append(
                'Cleartext file (%s) not found' % conf.get('cleartext_file')
            )
    if conf.get('running_mode', '').lower() not in (
                'encrypt', 'decrypt', 'cleanup',
                'write-exif', 'read-exif', 'dump-exif', 'clean-exif'
            ):
        errors.append(
            'Invalid running mode specified (%s)' % conf.get('running_mode')
        )
    if conf.get('data_source') not in ('file', 'terminal'):
        errors.append(
            'Invalid data source specified (%s)' % conf.get('data_source')
        )
    action_result.update({'exit': len(errors) + 10, 'msg': '\n'.join(errors)})
    return False if errors else True

# GENERAL

def shell_cmd(command, user=None):
    if user:
        command = "su %s -c \'%s\'" % (str(user), str(command))
    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    output, errors = process.communicate()
    return  str(output).rstrip('\n'), str(errors).rstrip('\n'), process.returncode

def message_to_bin(message):
    return ''.join(format(ord(char), '08b') for char in message)

#@pysnooper.snoop()
def load_config(file_path):
    global CONFIG
    if not file_path or not os.path.exists(file_path):
        return
    with open(file_path, 'r') as fl:
        CONFIG.update(json.load(fl))
    return CONFIG

#@pysnooper.snoop()
def file2list(file_path):
    if not file_path or not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as fl:
        converted = fl.readlines()
    return converted

#@pysnooper.snoop()
def write2file(*args, file_path=str(), mode='w', **kwargs):
    with open(file_path, mode, encoding='utf-8', errors='ignore') \
            as active_file:
        content = ''
        for line in args:
            content = content + (
                str(line) if '\n' in line else str(line) + '\n'
            )
        for line_key in kwargs:
            content = content + \
                str(line_key) + '=' + str(kwargs[line_key]) + '\n'
        try:
            active_file.write(content)
        except UnicodeError as e:
            return False
    return True

def clear_screen():
    return os.system('cls' if os.name == 'nt' else 'clear')

def stdout_msg(message, silence=False, red=False, info=False, warn=False,
            err=False, done=False, bold=False, green=False, ok=False, nok=False):
    if red:
        display_line = '\033[91m' + str(message) + '\033[0m'
    elif green:
        display_line = '\033[1;32m' + str(message) + '\033[0m'
    elif ok:
        display_line = '[ ' + '\033[1;32m' + 'OK' + '\033[0m' + ' ]: ' \
            + '\033[92m' + str(message) + '\033[0m'
    elif nok:
        display_line = '[ ' + '\033[91m' + 'NOK' + '\033[0m' + ' ]: ' \
            + '\033[91m' + str(message) + '\033[0m'
    elif info:
        display_line = '[ INFO ]: ' + str(message)
    elif warn:
        display_line = '[ ' + '\033[91m' + 'WARNING' + '\033[0m' + ' ]: ' \
            + '\033[91m' + str(message) + '\x1b[0m'
    elif err:
        display_line = '[ ' + '\033[91m' + 'ERROR' + '\033[0m' + ' ]: ' \
            + '\033[91m' + str(message) + '\033[0m'
    elif done:
        display_line = '[ ' + '\x1b[1;34m' + 'DONE' + '\033[0m' + ' ]: ' \
            + str(message)
    elif bold:
        display_line = '\x1b[1;37m' + str(message) + '\x1b[0m'
    else:
        display_line = message
    if silence:
        return False
    print(display_line)
    return True

# ACTIONS

# TODO - Add batch support
#@pysnooper.snoop()
def clean_exif(**context) -> str:
    global action_result
    failures = 0
    if context.get('in_line'):
        out_img_path = context['image_file']
    else:
        img_dir = os.path.dirname(context['image_file'])
        img_name = os.path.basename(context['image_file'])
        out_img_path = img_dir + '/hips.' + img_name
    try:
        image = Image.open(context['image_file'])
        # Check if the image has EXIF data
        if hasattr(image, '_getexif'):
            exif_dict = piexif.load(image.info["exif"])
            # Remove all EXIF data
            exif_dict = {}
            # Save the image without EXIF data to the specified output path
            image.save(out_img_path, exif=piexif.dump(exif_dict))
        # If the image doesn't have EXIF data attribute
        else:
            failures += 1
            action_result['errors'].append(
                f"Image {context['image_file']} does not have EXIF data."
            )
    except Exception as e:
        failures += 1
        action_result['errors'].append(str(e))
    action_result.update({
        'input': [context['image_file']],
        'output': [out_img_path] if os.path.exists(out_img_path) else [],
        'msg': 'OK: EXIF clean successful' if not failures \
            else 'NOK: EXIF clean failures detected (%s)' % failures,
        'exit': 0 if os.path.exists(out_img_path) and not failures else 9,
    })
    return out_img_path if not failures else None

# TODO - Add batch support
#@pysnooper.snoop()
def write_exif(**context) -> str:
    global action_result
    failures, tag_id = 0, context.get('exif_tag', piexif.ExifIFD.UserComment)
    if context.get('in_line'):
        out_img_path = context['image_file']
    else:
        img_dir = os.path.dirname(context['image_file'])
        img_name = os.path.basename(context['image_file'])
        out_img_path = img_dir + '/hips.' + img_name
    try:
        image = Image.open(context['image_file'])
        # Check if the image has EXIF data
        if hasattr(image, '_getexif'):
            exif_dict = piexif.load(image.info["exif"])
            # Set the specified tag ID with the provided value
            exif_dict['Exif'][tag_id] = context['exif_data'].encode('utf-8')
            # Convert the updated EXIF data back to bytes
            exif_bytes = piexif.dump(exif_dict)
            # Save the image with the updated EXIF data
            image.save(out_img_path, exif=exif_bytes)
        else:
            failures += 1
            action_result['errors'].append(
                f"Image {context['image_file']} does not have EXIF data."
            )
    except Exception as e:
        failures += 1
        action_result['errors'].append(str(e))
    action_result.update({
        'input': [context['image_file'], f'EXIF Tag: {tag_id}'],
        'output': [out_img_path, context['exif_data']]
            if os.path.exists(out_img_path) else [],
        'msg': 'OK: EXIF write successful' if not failures \
            else 'NOK: EXIF write failures detected (%s)' % failures,
        'exit': 0 if os.path.exists(out_img_path) and not failures else 9,
    })
    return out_img_path if not failures else None

# TODO - Add batch support
#@pysnooper.snoop()
def read_exif(**context) -> str:
    global action_result
    failures = 0
    tag_id, tag_data = context.get('exif_tag', piexif.ExifIFD.UserComment), ''
    try:
        # Open the image using PIL
        image = Image.open(context['image_file'])
        # Check if the image has EXIF data
        if hasattr(image, '_getexif'):
            exif_dict = piexif.load(image.info["exif"])
            # Check if the specified tag ID is present in the EXIF data
            if tag_id in exif_dict['Exif']:
                tag_data = exif_dict['Exif'][tag_id].decode('utf-8')
            else:
                failures += 1
                action_result['errors'].append(
                    f"Tag {tag_id} not found in the EXIF data."
                )
        # If the image doesn't have EXIF data attribute
        else:
            failures += 1
            action_result['errors'].append(
                f"Image {context['image_file']} does not have EXIF data."
            )
    except Exception as e:
        failures += 1
        action_result['errors'].append(str(e))
    action_result.update({
        'input': [context['image_file'], f'EXIF Tag: {tag_id}'],
        'output': [tag_data] if tag_data else [],
        'msg': 'OK: EXIF read successful' if not failures \
            else 'NOK: EXIF read failures detected (%s)' % failures,
        'exit': 0 if not failures else 9,
    })
    return tag_data if not failures else None

# TODO - Add batch support
#@pysnooper.snoop()
def dump_exif(**context) -> dict:
    global action_result
    failures, exif_data = 0, {}
    try:
        # Open the image using PIL
        image = Image.open(context['image_file'])
        # Check if the image has EXIF data
        if hasattr(image, '_getexif'):
            exif_details = piexif.load(image.info["exif"])
            for ifd, sub_dict in exif_details.items():
                if not sub_dict:
                    continue
                for tag, value in sub_dict.items():
                    exif_data[str(tag)] = str(value)
        # If the image doesn't have EXIF data attribute
        else:
            failures += 1
            action_result['errors'].append("The image does not have EXIF data.")
    except Exception as e:
        failures += 1
        action_result['errors'].append(str(e))
    action_result.update({
        'input': [context['image_file']],
        'output': [exif_data] if exif_data else [],
        'msg': 'OK: EXIF dump successful' if not failures \
            else 'NOK: EXIF dump failures detected (%s)' % failures,
        'exit': 0 if not failures else 9,
    })
    return exif_data if not failures else None

# TODO - Add batch support
#@pysnooper.snoop()
def encrypt(*data: List[str], **context) -> str:
    global action_result
    failures = 0
    if context.get('in_line'):
        out_img_path = context['image_file']
    else:
        img_dir = os.path.dirname(context['image_file'])
        img_name = os.path.basename(context['image_file'])
        out_img_path = img_dir + '/hips.' + img_name
    # If data is not a file that exists, it will be written to tmp_file
    if not os.path.exists(data[0]):
        with open(context['tmp_file'], 'w') as fl:
            fl.write(';'.join(data))
        secret_file = context['tmp_file']
    else:
        secret_file = data[0]
    if os.path.exists(out_img_path):
        os.remove(out_img_path)
    stdout, stderr, exit = shell_cmd(
        'steghide embed -ef %s -cf %s -sf %s -p %s' % (
            secret_file, context['image_file'], out_img_path, context['keycode']
        )
    )
    if exit != 0:
        action_result['errors'] += [stdout, stderr]
        failures += 1
    secret_content = ''.join(file2list(secret_file))
    action_result.update({
        'input': [context['image_file']],
        'output': [out_img_path, secret_content],
        'msg': 'OK: Encryption successful' if os.path.exists(out_img_path) and \
            not failures else 'NOK: Encryption failures detected (%s)' % failures,
        'exit': 0 if os.path.exists(out_img_path) and not failures else 9,
    })
    return out_img_path if not failures else None

# TODO - Add batch support
#@pysnooper.snoop()
def decrypt(**context) -> str:
    global action_result
    failures = 0
    stdout, stderr, exit = shell_cmd(
        'steghide extract -sf %s -p %s' % (
            context['image_file'], context['keycode']
        )
    )
    if exit != 0:
        action_result['errors'] += [stdout, stderr]
        failures += 1
    sanitized_stderr = stderr.lstrip('"b\'').rstrip('.\\n\'"').replace('"', '')
    action_result.update({
        'input': [context['image_file']],
        'output': [stdout if exit != 0 else sanitized_stderr],
        'msg': 'OK: Decryption successful' if not failures \
            else 'NOK: Decryption failures detected (%s)' % failures,
        'exit': 0 if not failures else 9,
    })
    revealed_file = sanitized_stderr.split(' ')[-1]
    if os.path.exists(revealed_file):
        content = '\n'.join(file2list(revealed_file))
        action_result['output'].append(content)
    return context['image_file'] if not failures else None

# FORMATTERS

def format_header():
    header = '''
_______________________________________________________________________________

  *              *             *  %s''' % SCRIPT_NAME + '''  *              *             *
________________________________________________________v%s%s_____________''' % (VERSION, VERSION_NAME) + '''
             Excellent Regards, the Alveare Solutions #!/Society -x
    '''
    return header

# DISPLAY

#@pysnooper.snoop()
def display2terminal(*lines, result=False, **context):
    if (not lines and not result) or context.get('silent'):
        return True
    if result:
        stdout_msg(
            '[ %s ]: %s Action Result' % (
                CONFIG.get('running_mode', '').upper(), SCRIPT_NAME
            ), silence=context.get('silent')
        )
        stdout_msg(
            json.dumps(action_result, indent=4), silence=context.get('silent')
        )
    else:
        stdout_msg('\n'.join(lines) + '\n', silence=context.get('silent'))
    print()
    return True

#@pysnooper.snoop()
def display_header(**context):
    if context.get('silent'):
        return False
    stdout_msg(format_header())
    return True

# CREATORS

#@pysnooper.snoop()
def create_command_line_parser():
    parser = optparse.OptionParser(
        format_header() + '\n[ DESCRIPTION ]: HIPSCipher Encryption/Decryption -\n\n'
        '    [ Ex ]: Terminal based running mode with default settings\n'
        '       ~$ %prog \n\n'
        '    [ Ex ]: File based running mode decryption\n'
        '       ~$ %prog \\ \n'
        '           --action decrypt \\ \n'
        '           --image-file target.jpg \\ \n'
        '           --key-code HIPS1234\n\n'
        '    [ Ex ]: File based running mode encryption with no STDOUT\n'
        '       ~$ %prog \\ \n'
        '           --action encrypt \\ \n'
        '           --image-file target.jpg \\ \n'
        '           --key-code HIPS1234 \\ \n'
        '           --cleartext-file hc_cleartext.txt \\ \n'
        '           --in-place \\ \n'
        '           --silent\n\n'
        '    [ Ex ]: File based running mode batch encryption with STDOUT\n'
        '       ~$ %prog \\ \n'
        '           --action encrypt \\ \n'
        '           --key-code HIPS1234 \\ \n'
        '           --batch \\ \n'
        '           --batch-dir files2encrypt \\ \n'
        '           --cleartext-file hc_cleartext.txt\n\n'
        '   [ Ex ]: File based EXIF dump saved to non-default report file\n'
        '       ~$ %prog \\ \n'
        '           --action dump-exif \\ \n'
        '           --image-file target.jpg \\ \n'
        '           --report \\ \n'
        '           --report-file hc_custom.report\n\n'
        '   [ Ex ]: File based EXIF write\n'
        '       ~$ %prog \\ \n'
        '           --action write-exif \\ \n'
        '           --exif-tag 37510 \\ \n'
        '           --exif-data #!/ \\ \n'
        '           --image-file target.jpg\n\n'
        '   [ Ex ]: File based EXIF tag read\n'
        '       ~$ %prog \\ \n'
        '           --action read-exif \\ \n'
        '           --exif-tag 37510 \\ \n'
        '           --image-file target.jpg\n\n'
        '   [ Ex ]: File based EXIF cleanup\n'
        '       ~$ %prog \\ \n'
        '           --action clean-exif \\ \n'
        '           --image-file target.jpg\n\n'
        '   [ Ex ]: Run with context data from JSON config file\n'
        '       ~$ %prog \\ \n'
        '           --konfig-file conf/hips_cipher.conf.json\n\n'
        '   [ Ex ]: Cleanup all generated files from disk\n'
        '       ~$ %prog \\ \n'
        '           --action cleanup'
    )
    return parser

# PARSERS

#@pysnooper.snoop()
def process_command_line_options(parser, **context):
    global CONFIG
    (options, args) = parser.parse_args()
    if options.config_file:
        return load_config(options.config_file)
    to_update = {key: val for key, val in options.__dict__.items() if val}
    CONFIG.update(to_update)
    return to_update

#@pysnooper.snoop()
def add_command_line_parser_options(parser):
    parser.add_option(
        '-a', '--action', dest='running_mode', type='string',
        help='Specify the desired action. Options: <encrypt|decrypt|cleanup>',
    )
    parser.add_option(
        '-i', '--image-file', dest='image_file', type='string',
        help='Path to the image file to operate on.'
    )
    parser.add_option(
        '-c', '--cleartext-file', dest='cleartext_file', type='string',
        help='Cleartext file path for IO operations during file running mode.'
    )
    parser.add_option(
        '-d', '--batch-dir', dest='batch_dir', type='string',
        help='Specify location to patch dirs of files.'
    )
    parser.add_option(
        '-x', '--exif-data', dest='exif_data', type='string',
        help='The exif data to write. (Implies --action write-exif, Default: #!/)'
    )
    parser.add_option(
        '-X', '--exif-tag', dest='exif_tag', type='string',
        help='The exif tag to write. (Implies --action (write-exif|read-exif), '
            'Default: [37510]UserComment)'
    )
    parser.add_option(
        '-s', '--data-src', dest='data_source', type='string',
        help='Specify if the input data source. Options: <file|terminal>, '
            'Default: file'
    )
    parser.add_option(
        '-R', '--report-file', dest='report_file', type='string',
        help='Specify path of report file. (Implies --report)'
    )
    parser.add_option(
        '-K', '--konfig-file', dest='config_file', type=str,
        help='Path to the %s configuration file.' % SCRIPT_NAME
    )
    parser.add_option(
        '-I', '--in-place', dest='in_place', action='store_true',
        help='Modify target image in place without creating copy.'
    )
    parser.add_option(
        '-b', '--batch', dest='batch', action='store_true',
        help='Perform actions on all files in the batch directory.'
    )
    parser.add_option(
        '-S', '--silent', dest='silent', action='store_true',
        help='Run with no STDOUT output. Implies a file data source.'
    )
    parser.add_option(
        '-r', '--report', dest='report', action='store_true',
        help='Save action results to report file.'
    )
    return parser

#@pysnooper.snoop()
def parse_cli_args(**context):
    parser = create_command_line_parser()
    add_command_line_parser_options(parser)
    return process_command_line_options(parser, **context)

# REPORTERS

def report_action_result(result, **context):
    return write2file(
        json.dumps(action_result, indent=4),
        file_path=context.get('report_file')
    )

# CLEANERS

#@pysnooper.snoop()
def cleanup(full=False, **context):
    global CONFIG
    global action_result
    to_remove = [
        context.get(label, '')
        for label in context['cleanup' if not full else 'full_cleanup']
    ]
    try:
        for file_path in to_remove:
            if not os.path.exists(file_path):
                continue
            os.remove(file_path)
        if full:
            CONFIG.update({'report': False})
    except OSError as e:
        action_result.update({
            'msg': 'Cleanup error! Details: %s' % str(e),
            'exit': 8,
        })
        return False
    return True

# SETUP

#@pysnooper.snoop()
def setup(**context):
    global action_result
    file_paths = ['cleartext_file']
    for fl_label in file_paths:
        if fl_label not in context or os.path.exists(context[fl_label]):
            continue
        try:
            create = write2file('', mode='a', file_path=context[fl_label])
        except Exception as e:
            action_result['errors'].append(str(e))
    if action_result['errors']:
        action_result.update({
            'msg': '%s Setup failed ' % SCRIPT_NAME +
                'with (%d) errors! Details: ' % len(errors) + ','.join(errors),
            'exit': 11,
        })
    return True if not action_result['errors'] else False

# INIT

#@pysnooper.snoop()
def init_terminal_running_mode(**conf):
    global action_result
    while True:
        action_result['errors'] = []
        if os.path.exists(conf['tmp_file']):
            os.remove(conf['tmp_file'])
        action = fetch_running_mode_from_user()
        if not action:
            action_result.update({
                'exit': 0,
                'msg': 'Action aborted at running mode prompt'
            })
            break
        if action == 'cleanup':
            clean = cleanup(full=True, **conf)
            clear = clear_screen()
            display_header(**conf)
            continue
        elif action not in (
                'dump-exif', 'read-exif', 'write-exif', 'cleanup', 'clean-exif'
            ):
            keycode = fetch_keycode_from_user()
            if not keycode:
                action_result.update({
                    'exit': 0,
                    'msg': 'Action aborted at keycode prompt'
                })
                break
        img_file = fetch_image_file_path_from_user()
        if not img_file:
            action_result.update({
                'exit': 0,
                'msg': 'Action aborted at image file input prompt'
            })
            break
        if action in ('encrypt', 'write-exif'):
            data = fetch_data_from_user()
            if not data:
                action_result.update({
                    'exit': 0,
                    'msg': 'Action aborted at data input prompt'
                })
                break
            if action == 'write-exif':
                CONFIG['exif_data'] = data
        if action in ('write-exif', 'read-exif'):
            exif_tag = fetch_exif_tag_from_user()
            if not exif_tag:
                action_result.update({
                    'exit': 0,
                    'msg': 'Action aborted at EXIF tag input prompt'
                })
                break
        handlers = {
            'encrypt': encrypt,
            'decrypt': decrypt,
            'write-exif': write_exif,
            'read-exif': read_exif,
            'dump-exif': dump_exif,
            'clean-exif': clean_exif,
        }
        if CONFIG.get('running_mode') not in handlers:
            action_result.update({
                'exit': 4,
                'msg': 'Invalid running mode %s' % CONFIG.get('running_mode')
            })
            return action_result['exit']

        # TODO - Handle batch action here

        if action == 'encrypt':
            action = handlers[CONFIG['running_mode']](data, **CONFIG)
        else:
            action = handlers[CONFIG['running_mode']](**CONFIG)

        if action is None:
            action_result.update({
                'exit': 5,
                'msg': 'Action %s failed' % CONFIG.get('running_mode')
            })
        display = display2terminal(result=True, **CONFIG)
        if not display:
            action_result.update({
                'exit': 7,
                'msg': 'Could not display action result'
            })
        replay = fetch_replay_confirmation_from_user()
        if not replay:
            break
        clear = clear_screen()
        display_header(**CONFIG)
    return action_result['exit']

#@pysnooper.snoop()
def init_file_running_mode(**conf):
    global action_result
    if not conf.get('keycode'):
        keycode = fetch_keycode_from_user()
    img_file = conf.get('image_file')
    if not os.path.exists(img_file):
        action_result.update({
            'exit': 2,
            'msg': 'Could not find image file %s' % img_file
        })
        return action_result['exit']
    if CONFIG.get('running_mode') == 'encrypt':
        data = ''.join(
            file2list(conf.get('cleartext_file', 'hc_cleartext.txt'))
        )
    handlers = {
        'encrypt': encrypt,
        'decrypt': decrypt,
        'write-exif': write_exif,
        'read-exif': read_exif,
        'dump-exif': dump_exif,
        'clean-exif': clean_exif,
    }
    if conf.get('running_mode') not in handlers:
        action_result.update({
            'exit': 4,
            'msg': 'Invalid running mode %s' % conf.get('running_mode')
        })
        return action_result['exit']

        # TODO - Handle batch action here

    args = [] if conf['running_mode'] != 'encrypt' else [conf['cleartext_file']]
    action = handlers[CONFIG['running_mode']](*args, **conf)

    if action is None:
        action_result.update({
            'exit': 5,
            'msg': 'Action %s failed' % CONFIG.get('running_mode')
        })
    display = display2terminal(result=True, **conf)
    if not display:
        action_result.update({
            'exit': 7,
            'msg': 'Could not display action result'
        })
    return action_result['exit']

#@pysnooper.snoop()
def init():
    global CONFIG
    global action_result
    cli_parse = parse_cli_args(**CONFIG)
    CONFIG['data_source'] = 'terminal' if not cli_parse \
        and not CONFIG['data_source'] else 'file'
    display_header(**CONFIG)
    stdout_msg(
        "[ INIT ]: Those who see beyond the Realm Of Forms leaped into the Jump Gate...\n",
        silence=CONFIG.get('silent')
    )
    try:
        lock_n_load = setup(**CONFIG)
        if CONFIG.get('running_mode', '').lower() == 'cleanup':
            stdout_msg(
                '[ ACTION ]: Cleaning up files from disk...',
                silence=CONFIG.get('silent')
            )
            clean = cleanup(full=True, **CONFIG)
            stdout_msg(
                'Terminating with exit code (%s)' % str(action_result['exit']),
                silence=CONFIG.get('silent'), done=True
            )
            exit(action_result['exit'])
        check = check_preconditions(**CONFIG)
        if not check:
            details = action_result.get('msg', '')
            action_result.update({
                'msg': 'Action preconditions check failed for running mode '\
                    '%s. Details: %s' % (CONFIG.get('running_mode'), details),
                'exit': 1,
            })
            exit(action_result['exit'])
        if not cli_parse or CONFIG.get('data_source').lower() == 'terminal':
            run = init_terminal_running_mode(**CONFIG)
        else:
            run = init_file_running_mode(**CONFIG)
    except Exception as e:
        action_result.update({'msg': str(e), 'exit': 10})
    finally:
        if CONFIG.get('cleanup'):
            clean = cleanup(**CONFIG)
        if CONFIG.get('report'):
            report = report_action_result(action_result, **CONFIG)
            if not report:
                action_result.update({
                    'msg': 'Failed to generate report %s'
                        % CONFIG.get('report_file'),
                    'exit': 20,
                })
    print(); stdout_msg(
        'Terminating with exit code (%s)' % str(action_result['exit']),
        silence=CONFIG.get('silent'), done=True
    )
    exit(action_result['exit'])


if __name__ == '__main__':
    init()


# CODE DUMP

