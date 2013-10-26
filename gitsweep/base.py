import subprocess


class MissingRemote(Exception):

    """Raise when a remote by name is not found."""


class MissingMasterBranch(Exception):

    """Raise when the "master" branch cannot be located."""


class InvalidGitRepositoryError(Exception):

    """Raise when not in a git repository."""


class Repo(object):

    """Contain git repository operations."""

    def __init__(self, path):
        self.path = path

    def remotes(self):
        """Return list of remotes."""
        return [line.strip() for line in git(['remote'],
                                             path=self.path).splitlines()]


def git(arguments, path):
    """Run git."""
    process = subprocess.Popen(
        ['git'] + arguments,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        cwd=path)

    result = process.communicate()

    if process.returncode != 0:
        raise InvalidGitRepositoryError()

    return result[0].decode('utf-8')


def fetch(remote, path):
    """Download objects and refs from remote repository."""
    git(['fetch', remote], path=path)


def remote_heads(remote, path):
    """Yield heads."""
    for line in git(['ls-remote', '--heads', remote], path=path).splitlines():
        text = line.split()[1]
        start = 'refs/heads/'
        assert text.startswith(start)
        yield text[len(start):]


class BaseOperation(object):

    """Base class for all Git-related operations."""

    def __init__(self, repo, remote_name='origin', master_branch='master'):
        self.repo = repo
        self.remote_name = remote_name
        self.master_branch = master_branch

    def _filtered_remotes(self, origin, skip=[]):
        """Returns a list of remote refs, skipping ones you don't need.

        If ``skip`` is empty, it will default to ``['HEAD',
        self.master_branch]``.

        """
        if not skip:
            skip = ['HEAD', self.master_branch]

        refs = [head for head in remote_heads(origin, self.repo.path)
                if not head in skip]

        return refs

    def _master_ref(self, origin):
        """Finds the master ref object that matches master branch."""
        for head in remote_heads(origin, self.repo.path):
            if head == self.master_branch:
                return head

        raise MissingMasterBranch(
            'Could not find ref for {0}'.format(self.master_branch))

    @property
    def _origin(self):
        """Gets the remote that references origin by name self.origin_name."""
        origin = None

        for remote in self.repo.remotes():
            if remote == self.remote_name:
                origin = remote

        if not origin:
            raise MissingRemote('Could not find the remote named {0}'.format(
                self.remote_name))

        return origin
