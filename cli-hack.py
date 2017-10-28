import sys

VERBOSE = True

if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser(description='Env Tracker')
    # parser.add_argument('command', metavar='command', help='command')
    # args = parser.parse_args()
    # command = args.command
    try:
        command = sys.argv[1]
    except Exception as e:
        exit('Must specify a command. See et.cli-hack.py for options')
    else:
        positional_args = sys.argv[2:]
        # TODO: no reason why we can't just have dynamic imports here
        try:
            if (command == 'init'):
                from commands.init import init
                init(*positional_args)
            elif (command == 'track'):
                from commands.track import track
                track(*positional_args)
            else:
                print('Unknown command: {0}'.format(command))
        except Exception as e:
            if VERBOSE:
                raise
            else:
                sys.exit(e)
