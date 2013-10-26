import subprocess

from .base import BaseOperation


class Inspector(BaseOperation):

    """Used to introspect a Git repository."""

    def merged_refs(self, skip=[]):
        """Returns a list of remote refs that have been merged into the master
        branch.

        The "master" branch may have a different name than master. The value of
        ``self.master_name`` is used to determine what this name is.

        """
        origin = self._origin

        master = self._master_ref(origin)
        refs = self._filtered_remotes(
            origin, skip=['HEAD', self.master_branch] + skip)
        merged = []

        for ref in refs:
            upstream = '{origin}/{master}'.format(
                origin=origin.name, master=master.remote_head)
            head = '{origin}/{branch}'.format(
                origin=origin.name, branch=ref.remote_head)
            # Drop to the git binary to do this, it's just easier to work with
            # at this level.
            process = subprocess.Popen(
                ['git', 'cherry', upstream, head],
                stdin=subprocess.PIPE,
                cwd=self.repo.working_dir,
                stdout=subprocess.PIPE)
            stdout = process.communicate()[0].decode('utf-8')
            if process.returncode == 0 and not stdout:
                # This means there are no commits in the branch that are not
                # also in the master branch. This is ready to be deleted.
                merged.append(ref)

        return merged
