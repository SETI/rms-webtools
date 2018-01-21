#!/usr/bin/env python
################################################################################
# re-validate.py
#
# Syntax:
#   re-validate.py path [path ...]
# 
# Enter the --help option to see more information.
################################################################################

import sys
import os
import glob
import argparse
import datetime
import socket
from smtplib import SMTP

import pdslogger
import pdsfile
import pdschecksums
import pdsarchives
import pdsinfoshelf
import pdslinkshelf
import pdsdependency

LOGNAME = 'pds.validation.re-validate'
LOGROOT_ENV = 'PDS_LOG_ROOT'

SERVER = 'list.seti.org'
FROM_ADDR = "PDS Administrator <pds-admin@seti.org>"
REPORT_SUBJ = "Re-validate report from " + socket.gethostname()
REPORT_SUBJ_W_ERRORS = "Re-validate report with ERRORs from " + \
                                              socket.gethostname()
ERROR_REPORT_SUBJ = "Re-validate ERROR report from " + socket.gethostname()

################################################################################
# Function to validate one volume
################################################################################

def validate_one_volume(pdsdir, voltypes, tests, namespace, logger):
    """Validates one volume."""

    tests_performed = 0

    # Open logger for this volume
    logfile = pdsdir.log_path_for_volume()
    logfile = logfile.replace('/volumes/', '/' + namespace.subdirectory)
    path_handler = pdslogger.file_handler(logfile)

    logger.blankline()
    logger.open('Re-validate ' + pdsdir.abspath, handler=path_handler)
    try:

        logger.info('Last modification', pdsdir.date)
        logger.info('Volume types', str(voltypes)[1:-1].replace("'",""))
        logger.info('Tests', str(tests)[1:-1].replace("'",""))
        logger.blankline()

        # Checksums and archives for each voltype...
        for voltype in voltypes:
            abspath = pdsdir.abspath.replace('/volumes/',
                                             '/' + voltype + '/')
            if not os.path.exists(abspath): continue

            temp_pdsdir = pdsfile.PdsFile.from_abspath(abspath)
            if namespace.checksums and not namespace.targz_only:
                logger.open('Checksum re-validatation for', abspath)
                try:
                    pdschecksums.validate(temp_pdsdir, None, logger)
                finally:
                    tests_performed += 1
                    logger.close()

            if namespace.archives and not namespace.targz_only:
                logger.open('Archive re-validatation for', abspath)
                try:
                    pdsarchives.validate(temp_pdsdir, logger)
                finally:
                    tests_performed += 1
                    logger.close()

        # Checksums for each 'archive-' + voltype...
        if checksums and targz:
            for voltype in voltypes:
                abspath = pdsdir.abspath.replace('/volumes/',
                                                 '/archives-' + voltype + '/')
                abspath += '*.tar.gz'
                abspath = glob.glob(abspath)
                if not abspath: continue

                abspath = abspath[0]

                (prefix, basename) = os.path.split(abspath)
                temp_pdsdir = pdsfile.PdsFile.from_abspath(prefix)
                logger.open('Checksum re-validatation for', abspath)
                try:
                    pdschecksums.validate(temp_pdsdir, basename, logger)
                finally:
                    tests_performed += 1
                    logger.close()

        # Infoshelves and linkshelves for each voltype...
        for voltype in voltypes:
            abspath = pdsdir.abspath.replace('/volumes/',
                                             '/' + voltype + '/')
            if not os.path.exists(abspath): continue

            temp_pdsdir = pdsfile.PdsFile.from_abspath(abspath)
            if namespace.infoshelves and not namespace.targz_only:
                logger.open('Infoshelf re-validatation for', abspath)
                try:
                    pdsinfoshelf.validate(temp_pdsdir, None, logger)
                finally:
                    tests_performed += 1
                    logger.close()

            if (namespace.linkshelves and not namespace.targz_only and
                voltype in ('volumes', 'calibrated', 'metadata')):
                    logger.open('Linkshelf re-validatation for', abspath)
                    try:
                        pdslinkshelf.validate(temp_pdsdir, logger)
                    finally:
                        tests_performed += 1
                        logger.close()

        # Infoshelves for each 'archive-' + voltype...
        if namespace.infoshelves and targz:
            for voltype in voltypes:
                abspath = pdsdir.abspath.replace('/volumes/',
                                                 '/archives-' + voltype + '/')
                abspath += '*.tar.gz'
                abspath = glob.glob(abspath)
                if not abspath: continue

                abspath = abspath[0]

                (prefix, basename) = os.path.split(abspath)
                temp_pdsdir = pdsfile.PdsFile.from_abspath(prefix)
                logger.open('Infoshelf re-validatation for', abspath)
                try:
                    pdsinfoshelf.validate(temp_pdsdir, basename, logger)
                finally:
                    tests_performed += 1
                    logger.close()

        # Dependencies
        if namespace.dependencies and not namespace.targz_only:
            logger.open('Dependency re-validation for', abspath)
            try:
                pdsdependency.test(pdsdir, logger)
            finally:
                tests_performed += 1
                logger.close()

    except Exception as e:
        logger.exception(e)

    finally:
        if tests_performed == 1:
            logger.info('1 re-validation test performed', pdsdir.abspath)
        else:
            logger.info('%d re-validation tests performed' % tests_performed,
                        pdsdir.abspath)
        (fatal, errors, warnings, tests) = logger.close()

    return (logfile, fatal, errors)

################################################################################
# Log and volume management for batch mode
################################################################################

def get_log_info(logfile):
    """Return info from the log:
        (start, elapsed, modtime, abspath, had_error, had_fatal).
    """

    with open(logfile) as f:
        recs = f.readlines()

    if not recs:
        raise ValueError('Empty log file: ' + logfile)

    parts = recs[0].split('|')
    if len(parts) < 2:
        raise ValueError('Empty log file: ' + logfile)

    start_time = parts[0].rstrip()
    if parts[1].strip() != LOGNAME:
        raise ValueError('Not a re-validate log file')

    abspath = parts[-1].strip().split(' ')[-1]

    if len(recs) < 1:
        raise ValueError('Not a re-validate log file')

    if 'Last modification' not in recs[1]:
        raise ValueError('Missing modification time')

    modtime = recs[1].split('modification:')[-1].strip()

    error = False
    fatal = False
    elapsed = None
    for rec in recs:
        error |= ('| ERROR |' in rec)
        fatal |= ('| FATAL |' in rec)

        k = rec.find('Elapsed time = ')
        if k >= 0:
            elapsed = rec[k + len('Elapsed time = '):].strip()

    if elapsed is None:
        fatal = True

    return (start_time, elapsed, modtime, abspath, error, fatal)

def get_all_log_info(logroot):
    """Read every log file below this root directory; return a list of tuples
    (start, elapsed, modtime, abspath, had_error, had_fatal)."""

    info_list = []
    for (root, dirs, files) in os.walk(logroot):
        for file in files:
            if not file.endswith('.log'): continue
            logfile = os.path.join(root, file)
            try:
                info = get_log_info(logfile)
            except Exception as e:
                if not isinstance(e, ValueError):
                    print logfile, e
                continue

            info_list.append(info)

    return info_list

def sort_log_info(info_list):
    """Sort log info, eliminating duplcated volume paths except most recent and
    ignoring fatal errors, from least to most recent."""

    last_info_for_abspath = {}
    for info in info_list:
        (start, elapsed, modtime, abspath, had_error, had_fatal) = info
        if had_fatal: continue

        if abspath in last_info_for_abspath:
            if start < last_info_for_abspath[abspath][0]: continue

        last_info_for_abspath[abspath] = info

    new_info = last_info_for_abspath.values()
    new_info.sort()
    return new_info

def get_volume_info(holdings):
    """Return a list of tuples (volume abspath, modtime) for every volume in
    the given holdings directory."""

    path = os.path.join(holdings, 'volumes/*_*/*_*')
    abspaths = glob.glob(path)

    info_list = []
    for abspath in abspaths:
        pdsdir = pdsfile.PdsFile.from_abspath(abspath)
        info_list.append((abspath, pdsdir.date))

    return info_list

def find_modified_volumes(holdings_info, log_info):
    """Compare the information in the holdings info and log info; return a tuple
    (modified_holdings, current_log_info)."""

    log_modtimes = set()
    log_dict = {}
    for info in log_info:
        (start, elapsed, modtime, abspath, had_error, had_fatal) = info
        log_modtimes.add((modtime, abspath))
        log_dict[abspath] = info

    holdings_modtimes = set()
    for (abspath, modtime) in holdings_info:
        holdings_modtimes.add((modtime, abspath))   # time before path, for sort

    modified_holdings = holdings_modtimes - log_modtimes
    modified_holdings = list(modified_holdings)
    modified_holdings.sort()    # from oldest to newest

    # Reverse to (abspath, modtime)
    modified_holdings = [(info[1],info[0]) for info in modified_holdings]

    # Delete these keys from log info
    for (key,modtime) in modified_holdings:
        if key in log_dict:
            del log_dict[key]

    # Sort the logged volumes from oldest to newest
    current_log_info = log_dict.values()
    current_log_info.sort()

    return (modified_holdings, current_log_info)

def send_email(to_addr, subject, message):
    smtp = SMTP()
    smtp.connect(SERVER, 25)
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if type(to_addr) == str:
        to_addr = [to_addr]

    to_addr_in_msg = ','.join(to_addr)

    msg = ("From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" \
           % (FROM_ADDR, to_addr_in_msg, subject, date, message))

    for addr in to_addr:
        smtp.sendmail(FROM_ADDR, addr, msg)

    smtp.quit()

################################################################################
# Executable program
################################################################################

# Set up parser
parser = argparse.ArgumentParser(
    description='re-validate: Perform various validation tasks on an online '  +
                'volume or volumes.')

parser.add_argument('volume', nargs='*', type=str,
                    help='Paths to volumes or volume sets for validation.')

parser.add_argument('--log', '-l', type=str, default='',
                    help='Root directory for the log files. Log files are '    +
                         'written to the "re-validate" subdirectory of this '  +
                         'directory. If not specified, logs are written to '   +
                         '"re-validate" subdirectory of the path defined by '  +
                         'environoment variable "%s". ' % LOGROOT_ENV          +
                         'If this is undefined, logs are written to the '      +
                         '"Logs/re-validate" subdirectory of the current '     +
                         'working directory.')

parser.add_argument('--subdirectory', '-s', type=str, default='',
                    help='Optional subdirectory below "re-validate" in which ' +
                         'write the log file. This can be used to organize '   +
                         'the results of different validation options.')

parser.add_argument('--batch', '-b', action='store_true',
                    help='Operate in batch mode. In this mode, the program '   +
                         'searches the existing logs and the given holdings '  +
                         'directories and validates any new volumes found. '   +
                         'Afterward, it validates volumes starting with the '  +
                         'ones with the oldest logs. Use --minutes to limit '  +
                         'the duration of the run.')

parser.add_argument('--minutes', type=int, default=60,
                    help='In batch mode, this is the rough upper limit of '    +
                         'the duration of the run. The program will iterate '  +
                         'through available volumes but will not start a new ' +
                         'one once the time limit in minutes has been reached.')

parser.add_argument('--batch-status',  action='store_true',
                    help='Prints a summary of what the program would do now '  +
                         'if run in batch mode.')

parser.add_argument('--email', type=str, action='append', default=[],
                    metavar='ADDR',
                    help='Email address to which to send a report when a '     +
                         'batch job completes. Repeat for multiple recipients.')

parser.add_argument('--error-email',  type=str, action='append', default=[],
                    metavar='ADDR',
                    help='Email address to which to send an error report '     +
                         'when a batch job completes. If no errors are '       +
                         'found, no message is sent. Repeat for multiple '     +
                         'recipients.')

parser.add_argument('--quiet', '-q', action='store_true',
                    help='Do not log to the terminal.')

parser.add_argument('--checksums', '-C', action='store_true',
                    help='Validate MD5 checksums.')

parser.add_argument('--archives', '-A', action='store_true',
                    help='Validate archive files.')

parser.add_argument('--info', '-I', action='store_true',
                    help='Validate infoshelves.')

parser.add_argument('--links', '-L', action='store_true',
                    help='Validate linkshelves.')

parser.add_argument('--dependencies', '-D', action='store_true',
                    help='Validate dependencies.')

parser.add_argument('--full', '-F', action='store_true',
                    help='Perform the full set of validation tests.')

parser.add_argument('--volumes', '-v', action='store_true',
                    help='Check volume directories.')

parser.add_argument('--calibrated', '-c', action='store_true',
                    help='Check calibrated directories.')

parser.add_argument('--diagrams', '-d', action='store_true',
                    help='Check diagram directories.')

parser.add_argument('--metadata', '-m', action='store_true',
                    help='Check metadata directories.')

parser.add_argument('--previews', '-p', action='store_true',
                    help='Check preview directories.')

parser.add_argument('--targz', '-t', action='store_true',
                    help='Check .tar.gz archives in addition to directories.')

parser.add_argument('--targz-only', '-T', action='store_true',
                    help='Only check .tar.gz checksums, not other files or '   +
                         'directories.')

parser.add_argument('--all', '-a', action='store_true',
                    help='Check all directories and files related to the '     +
                         'volume.')

# Parse and validate the command line
namespace = parser.parse_args()

# Interpret file types
voltypes = []
if namespace.volumes:
    voltypes += ['volumes']
if namespace.calibrated:
    voltypes += ['calibrated']
if namespace.diagrams:
    voltypes += ['diagrams']
if namespace.metadata:
    voltypes += ['metadata']
if namespace.calibrated:
    voltypes += ['previews']

if voltypes == [] or namespace.all:
    voltypes = ['volumes', 'calibrated', 'diagrams', 'metadata', 'previews']

targz = namespace.all or namespace.targz or namespace.targz_only

# Determine which tests to perform
checksums    = namespace.checksums
archives     = namespace.archives
infoshelves  = namespace.info
linkshelves  = namespace.links
dependencies = namespace.dependencies

if namespace.full or not (checksums or archives or infoshelves or linkshelves or
                          dependencies):
    checksums    = True
    archives     = True
    infoshelves  = True
    linkshelves  = True
    dependencies = True

checksums    |= (namespace.targz_only and not infoshelves)
archives     &= not namespace.targz_only
dependencies &= ('volumes' in voltypes and not namespace.targz_only)
linkshelves  &= (('volumes' in voltypes or 'metadata' in voltypes or
                                           'calibrated' in voltypes) and
                 not namespace.targz_only)

namespace.checksums    = checksums
namespace.archives     = archives
namespace.infoshelves  = infoshelves
namespace.linkshelves  = linkshelves
namespace.dependencies = dependencies

tests = []
if checksums   : tests.append('checksums')
if archives    : tests.append('archives')
if infoshelves : tests.append('infoshelves')
if linkshelves : tests.append('linkshelves')
if dependencies: tests.append('dependencies')
if namespace.targz_only: tests = ['checksums (tar.gz only)']

# Define the logging directory
if namespace.log:
    log_root_ = namespace.log.rstrip('/') + '/'
else:
    try:
        log_root_ = os.environ[LOGROOT_ENV].rstrip('/') + '/'
    except KeyError:
        log_root_ = 'Logs/'

namespace.log = log_root_ + 're-validate/'

if namespace.subdirectory:
    subdirectory_ = namespace.subdirectory.rstrip('/') + '/'
else:
    subdirectory_ = ''

namespace.subdirectory = subdirectory_

# Initialize logger
pdsfile.PdsFile.set_log_root(namespace.log)
new_limits = {'info':10, 'normal':10, 'override':False}
logger = pdslogger.PdsLogger(LOGNAME, limits=new_limits)

if not namespace.quiet:
    logger.add_handler(pdslogger.stdout_handler)

warning_handler = pdslogger.warning_handler(namespace.log)
logger.add_handler(warning_handler)

error_handler = pdslogger.error_handler(namespace.log)
logger.add_handler(error_handler)

########################################
# Interactive mode
########################################

if not namespace.batch and not namespace.batch_status:

    # Stop if a volume or volume set doesn't exist
    if not namespace.volume:
        print 'Missing volume path'
        sys.exit(1)

    for volume in namespace.volume:
        if not os.path.exists(volume):
            print 'Volume path not found: ' + volume
            sys.exit(1)

    # Convert to PdsFile objects; expand volume sets; collect holdings paths
    pdsdirs = []
    roots = set()
    for volume in namespace.volume:
        abspath = os.path.abspath(volume)
        pdsdir = pdsfile.PdsFile.from_abspath(abspath)
        if pdsdir.category_ != 'volumes/' or pdsdir.interior:
            print 'Not a volume path: ', pdsdir.abspath
            sys.exit(1)

        logger.add_root(pdsdir.root_)

        if pdsdir.volname:
            pdsdirs.append(pdsdir)
        else:
            for name in pdsdir.childnames:
                pdsdirs.append(pdsdir.child(name))

    # Main loop
    logger.open(' '.join(sys.argv))
    try:
        # For each volume...
        for pdsdir in pdsdirs:
            _ = validate_one_volume(pdsdir, voltypes, tests, namespace, logger)

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        (fatal, errors, warnings, tests) = logger.close()
        status = 1 if (fatal or errors) else 0

    sys.exit(status)

########################################
# Batch mode
########################################

else:

    # Find the holdings directory
    if not namespace.volume:
        namespace.volume = glob.glob('/Volumes/pdsdata*/holdings')

    if not namespace.volume:
        print 'No holdings path found'
        sys.exit(1)

    for holding in namespace.volume:
        if not os.path.exists(holding):
            print 'Holdings path not found: ' + holding
            sys.exit(1)

    logger.add_root(namespace.volume)

    # Read the existing logs
    log_info = get_all_log_info(namespace.log)
    log_info = sort_log_info(log_info)

    # Read the current holdings
    holdings_info = []
    for holding in namespace.volume:
        holdings_info += get_volume_info(holding)

    # Define an ordered list of tasks
    (modified_holdings,
     current_logs) = find_modified_volumes(holdings_info, log_info)

    # Print info in trial run mode
    if namespace.batch_status:
        fmt = '%4d %20s/%-11s  modified %s, not previously validated'
        line_number = 0
        for (abspath, date) in modified_holdings:
            pdsdir = pdsfile.PdsFile.from_abspath(abspath)
            line_number += 1
            print fmt % (line_number, pdsdir.volset_, pdsdir.volname,
                         date[:10])

        fmt ='%4d  %20s%-11s  modified %s, last validated %s, duration %s%s'
        for info in current_logs:
            (start, elapsed, date, abspath, had_error, had_fatal) = info
            pdsdir = pdsfile.PdsFile.from_abspath(abspath)
            error_text = ', error logged' if had_error else ''
            line_number += 1
            print fmt % (line_number, pdsdir.volset_, pdsdir.volname,
                         date[:10], start[:10], elapsed[:-7], error_text)

        sys.exit()

    # Start batch processing
    # info = (abspath, mod_date, prev_validation, had_errors)
    info = [(p[0], p[1], None, False) for p in modified_holdings] + \
           [(p[3], p[2], p[0], p[4]) for p in current_logs]
    start = datetime.datetime.now()

    batch_messages = []
    error_messages = []
    batch_prefix = ('Batch re-validate started at %s\n' %
                    start.strftime("%Y-%m-%d %H:%M:%S"))
    print batch_prefix

    # Main loop
    logger.open(' '.join(sys.argv))
    try:

        # For each volume...
        for (abspath, mod_date, prev_validation, had_errors) in info:
            pdsdir = pdsfile.PdsFile.from_abspath(abspath)
            if prev_validation is None:
                ps = 'not previously validated'
            else:
                ps = 'last validated %s' % prev_validation[:10]
            batch_message = '%20s%-11s  modified %s, %s' % \
                            (pdsdir.volset_, pdsdir.volname, mod_date[:10], ps)
            print batch_message

            (logfile,
             fatal, errors) = validate_one_volume(pdsdir, voltypes, tests,
                                                  namespace, logger)
            error_message = ''
            if fatal or errors:
                stringlist = ['***** ']
                if fatal:
                    stringlist += ['Fatal = ', str(fatal), '; ']
                if errors:
                    stringlist += ['Errors = ', str(errors), '; ']
                stringlist.append(logfile)
                error_message = ''.join(stringlist)

                print error_message

            batch_messages.append(batch_message)

            if error_message:
                batch_messages.append(error_message)

                error_messages.append(batch_message)
                error_messages.append(error_message)

            now = datetime.datetime.now()
            if (now - start).seconds > namespace.minutes*60:
                break

    except (Exception, KeyboardInterrupt) as e:
        logger.exception(e)
        raise

    finally:
        (fatal, errors, warnings, tests) = logger.close()
        status = 1 if (fatal or errors) else 0

        now = datetime.datetime.now()
        batch_suffix = ('\nTimeout at %s after %d minutes' %
                         (now.strftime("%Y-%m-%d %H:%M:%S"),
                         int((now - start).seconds/60. + 0.5)))
        print batch_suffix

        if namespace.email:
            if error_messages:
                subj = REPORT_SUBJ_W_ERRORS
            else:
                subj = REPORT_SUBJ

            full_message = [batch_prefix] + batch_messages + [batch_suffix]
            send_email(namespace.email, subj, '\n'.join(full_message))

        if error_messages and namespace.error_email:
            full_message = [batch_prefix] + error_messages + [batch_suffix]
            send_email(namespace.error_email, ERROR_REPORT_SUBJ,
                                              '\n'.join(full_message))

    sys.exit(status)

