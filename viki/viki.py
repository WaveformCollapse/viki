#!/usr/bin/env python3

"""
Viki cli
~~~~~~~~

The automation framework

Usage:
    viki h|help
    viki ll|list
    viki r|run <job_name>
    viki c|create <job_name>
    viki o|output <job_name>

Maintainer:
    John Shanahan <shanahan.jrs@gmail.com>

License:
    Apache 2.0
    http://www.apache.org/licenses/LICENSE-2.0
"""

__author__ = 'John Shanahan'
__author_email__ = 'shanahan.jrs@gmail.com'
__version__ = '0.1.1'

# --- Imports
import requests

# --- Setup
debug = True

# --- Private funcs

def _version():
    print({"name":"viki", "version":__version__})


def _usage():
    """ Print viki-cli usage"""
    print('Usage:')
    print('    viki h|help')
    print('    viki ll|list')
    print('    viki r|run <job_name>')
    sys.exit(1)


def _list():
    ret = job.get_jobs()
    return str(ret)


def _run(job_name, job_args=None):
    """
    :param job_name: Name of job to be run
    :param job_args: List of arguments to send with the job to be injected at run time
    :return:
    """
    ret = job.run_job(job_name, job_args)
    return str(ret)

def _output(job_name):
    """
    :param job_name:
    :return:
    """
    ret = job.get_last_run_output_by_name(job_name)
    return ret

# --- Main

def main(args):
    """ Main """
    message = "Ok"
    success = 1

    try:

        if len(args) < 2:
            _usage()

        # Possible args
        action_setup = ['setup', '-setup', '--setup']
        action_help = ['h', '-h', '--h', 'help', '-help', '--help']
        action_list = ['l', '-l', '--l', 'll', '-ll', '--ll', 'list', '-list', '--list']
        action_run = ['r', '-r', '--r', 'run', '-run', '--run']
        action_create = ['c', 'create', '-create', '--create']
        action_output = ['o', '-o', '--o', 'output', '-output', '--output']

        # Grab first positional arg
        command = args[1]

        # If they are running setup, make sure this gets done first
        if command in action_setup:
            _setup()

        # Check system setup has been run
        # TODO This needs some tuning. It currently still creates the files/dirs as root
        # and they need to be writable by other users or owned by another user (you, preferably)
        if not application.check_system_setup():
            print('System setup check failed')
            print('Please run viki setup script:')
            print('    `sudo viki setup\'')
            sys.exit(1)

        # --- Main execution

        if command in action_help:
            # Help/usage
            _usage()

        elif command in action_list:
            # List jobs
            message = str(_list())

        elif command in action_run:
            # Run a job
            job_name = args[2]

            if len(args) > 3:
                job_args = sys.argv[3:]
                message = str(_run(job_name, job_args))
            else:
                message = str(_run(job_name))

        elif command in action_create:
            # Create a new job
            # Not yet implemented
            message = "-- Not yet implemented --"
            pass

        elif command in action_output:
            # Show the output of the last run of the specified job
            message = str(_output(args[2]))

        else:
            # 404 Command not found
            _usage()

    except IndexError as error:
        message = str(error)
        success = 0

    # Fin
    print(message)


if __name__ == "__main__":
    print('Version: ' + version)
    main(sys.argv)
