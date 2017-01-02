import os

if __name__ == '__main__':
    # import argparse
    # parser = argparse.ArgumentParser(description='Env Tracker')
    # parser.add_argument('command', metavar='command', help='command')
    # args = parser.parse_args()
    # command = args.command
    try:
        import sys
        command = sys.argv[1]
    except Exception as e:
        exit('Must specify a command')
    else:
        positional_args = sys.argv[2:]
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
            raise
