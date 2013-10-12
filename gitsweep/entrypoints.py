import sys

from gitsweep import cli


def main():
    """Command-line interface."""
    return cli.run(sys.argv)


def test():
    """Run git-sweep's test suite."""
    import nose
    nose.main(argv=['nose'] + sys.argv[1:])
