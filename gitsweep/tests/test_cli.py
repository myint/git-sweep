from mock import patch

from gitsweep.tests.testcases import CommandTestCase


class TestHelpMenu(CommandTestCase):

    """Command-line tool can show the help menu."""

    def test_help(self):
        (retcode, stdout, stderr) = self.gscommand('git-sweep -h')

        self.assertTrue(stdout)

    def test_fetch(self):
        """Will fetch if told not to."""
        (retcode, stdout, stderr) = self.gscommand('git-sweep --dry-run')

        self.assertResults('''
            Fetching from the remote
            No remote branches are available for cleaning up
            ''', stdout)

    def test_no_fetch(self):
        """Will not fetch if told not to."""
        (retcode, stdout, stderr) = self.gscommand(
            'git-sweep --dry-run --nofetch')

        self.assertResults('''
            No remote branches are available for cleaning up
            ''', stdout)

    def test_will_preview(self):
        """Will preview the proposed deletes."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        (retcode, stdout, stderr) = self.gscommand('git-sweep --dry-run')

        self.assertResults('''
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            To delete them, run again without --dry-run
            ''', stdout)

    def test_will_preserve_arguments(self):
        """The recommended cleanup command contains the same arguments
        given."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        preview = 'git-sweep --dry-run --master=master --origin=origin'
        cleanup = 'git-sweep --master=master --origin=origin'

        (retcode, stdout, stderr) = self.gscommand(preview)

        self.assertResults('''
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            To delete them, run again without --dry-run
            '''.format(cleanup), stdout)

    def test_will_preview_none_found(self):
        """Will preview the proposed deletes."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')

        (retcode, stdout, stderr) = self.gscommand('git-sweep --dry-run')

        self.assertResults('''
            Fetching from the remote
            No remote branches are available for cleaning up
            ''', stdout)

    def test_will_cleanup(self):
        """Will preview the proposed deletes."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        with patch('gitsweep.cli.raw_input', create=True) as ri:
            ri.return_value = 'y'
            (retcode, stdout, stderr) = self.gscommand('git-sweep')

        self.assertResults('''
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            Delete these branches? (y/n) 
              deleting branch1 (done)
              deleting branch2 (done)
              deleting branch3 (done)
              deleting branch4 (done)
              deleting branch5 (done)

            All done!

            Tell everyone to run `git fetch --prune` to sync with this remote.
            (you don't have to, yours is synced)
            ''', stdout)

    def test_will_abort_cleanup(self):
        """Will preview the proposed deletes."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        with patch('gitsweep.cli.raw_input', create=True) as ri:
            ri.return_value = 'n'
            (retcode, stdout, stderr) = self.gscommand('git-sweep')

        self.assertResults('''
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

            Delete these branches? (y/n) 
            OK, aborting.
            ''', stdout)

    def test_will_skip_certain_branches(self):
        """Can be forced to skip certain branches."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        (retcode, stdout, stderr) = self.gscommand(
            'git-sweep --dry-run --skip=branch1,branch2')

        cleanup = 'git-sweep --skip=branch1,branch2'

        self.assertResults('''
            Fetching from the remote
            These branches have been merged into master:

              branch3
              branch4
              branch5

            To delete them, run again without --dry-run
            '''.format(cleanup), stdout)

    def test_will_force_clean(self):
        """Will cleanup immediately if forced."""
        for i in range(1, 6):
            self.command('git checkout -b branch{0}'.format(i))
            self.make_commit()
            self.command('git checkout master')
            self.make_commit()
            self.command('git merge branch{0}'.format(i))

        (retcode, stdout, stderr) = self.gscommand('git-sweep --force')

        self.assertResults('''
            Fetching from the remote
            These branches have been merged into master:

              branch1
              branch2
              branch3
              branch4
              branch5

              deleting branch1 (done)
              deleting branch2 (done)
              deleting branch3 (done)
              deleting branch4 (done)
              deleting branch5 (done)

            All done!

            Tell everyone to run `git fetch --prune` to sync with this remote.
            (you don't have to, yours is synced)
            ''', stdout)
