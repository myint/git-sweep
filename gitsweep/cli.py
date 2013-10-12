import sys
from os import getcwd
from argparse import ArgumentParser

from git import Repo, InvalidGitRepositoryError

from gitsweep.inspector import Inspector
from gitsweep.deleter import Deleter


class CommandLine(object):

    """Main interface to the command-line for running git-sweep."""
    parser = ArgumentParser(
        description='Clean up your Git remote branches.',
        prog='git-sweep'
    )

    _origin_kwargs = {
        'help': 'name of the remote you wish to clean up',
        'dest': 'origin',
        'default': 'origin'}

    _master_kwargs = {
        'help': 'name of what you consider the master branch',
        'dest': 'master',
        'default': 'master'}

    _skip_kwargs = {
        'help': 'comma-separated list of branches to skip',
        'dest': 'skips',
        'default': ''}

    _no_fetch_kwargs = {
        'help': 'do not fetch from the remote',
        'dest': 'fetch',
        'action': 'store_false',
        'default': True}

    parser.add_argument('--force', action='store_true', default=False,
                        dest='force', help='do not ask, cleanup immediately')
    parser.add_argument('--origin', **_origin_kwargs)
    parser.add_argument('--master', **_master_kwargs)
    parser.add_argument('--no-fetch', **_no_fetch_kwargs)
    parser.add_argument('--skip', **_skip_kwargs)
    parser.add_argument('--dry-run', action='store_true',
                        help='show what would be swept')

    def __init__(self, args):
        self.args = args[1:]

    def run(self):
        """Runs git-sweep."""
        try:
            self._sweep()
            sys.exit(0)
        except InvalidGitRepositoryError:
            sys.stderr.write('This is not a Git repository\n')

        sys.exit(1)

    def _sweep(self):
        """Runs git-sweep."""
        args = self.parser.parse_args(self.args)

        fetch = args.fetch
        skips = [i.strip() for i in args.skips.split(',')]

        # Is this a Git repository?
        repo = Repo(getcwd())

        remote_name = args.origin

        # Fetch from the remote so that we have the latest commits
        if fetch:
            for remote in repo.remotes:
                if remote.name == remote_name:
                    sys.stdout.write('Fetching from the remote\n')
                    remote.fetch()

        master_branch = args.master

        # Find branches that could be merged
        inspector = Inspector(repo, remote_name=remote_name,
                              master_branch=master_branch)
        ok_to_delete = inspector.merged_refs(skip=skips)

        if ok_to_delete:
            sys.stdout.write(
                'These branches have been merged into {0}:\n\n'.format(
                    master_branch))
        else:
            sys.stdout.write('No remote branches are available for '
                             'cleaning up\n')
            return

        for ref in ok_to_delete:
            sys.stdout.write('  {0}\n'.format(ref.remote_head))

        if not args.dry_run:
            deleter = Deleter(repo, remote_name=remote_name,
                              master_branch=master_branch)

            if not args.force:
                sys.stdout.write('\nDelete these branches? (y/n) ')
                answer = raw_input()
            if args.force or answer.lower().startswith('y'):
                sys.stdout.write('\n')
                for ref in ok_to_delete:
                    sys.stdout.write('  deleting {0}'.format(ref.remote_head))
                    deleter.remove_remote_refs([ref])
                    sys.stdout.write(' (done)\n')

                sys.stdout.write('\nAll done!\n')
                sys.stdout.write('\nTell everyone to run `git fetch --prune` '
                                 'to sync with this remote.\n')
                sys.stdout.write('(you don\'t have to, yours is synced)\n')
            else:
                sys.stdout.write('\nOK, aborting.\n')
        elif ok_to_delete:
            sys.stdout.write('\nTo delete them, run again without --dry-run\n')
