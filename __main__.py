if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Env Tracker')
    parser.add_argument('command', metavar='command', help='command')
    args = parser.parse_args()
    command = args.command

    if (command == 'init'):
        from commands.init import init
        init()
    else:
        print('Unknown command: {0}'.format(command))
