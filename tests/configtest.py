import os
from tempfile import mkdtemp, mkstemp
from random import randint

from avocado import Test
from avocado.utils import process


class Link(object):
    """Serves as a dummy Slave Link for testing"""
    def __init__(self, bin_dir, master=None):
        self.name = 'prog' + str(randint(0, 9999))
        self.path = mkstemp()[1]
        self.program_dir = mkdtemp()
        self.link = os.path.join(bin_dir, self.name)
        if master:
            self.master = master
            self.master.slaves.append(self)

    def __str__(self):
        """Convert Link info to command line format used by alternatives"""
        cmd = ' '.join(['--slave', self.link, self.name, self.path])
        return cmd


class MasterLink(Link):
    """Serves as a dummy Master Link for testing"""
    def __init__(self, bin_dir, priority=randint(1, 9999)):
        super(MasterLink, self).__init__(bin_dir)
        self.priority = priority
        self.slaves = []

    def __str__(self):
        """Convert Master Link info to command line format used by alternatives"""
        cmd = ' '.join([self.link, self.name, self.path, str(self.priority)])
        return cmd


class ConfigTest(Test):

    def setUp(self):
        self.alt_dir = mkdtemp()
        self.admin_dir = mkdtemp()
        self.bin_dir = mkdtemp()
        self.alternatives_path = os.environ['ALTERNATIVES_BINARY']

        self.log.info("BaseTest setup() executed")

    def alternatives_install(self, links):
        try:
            process.run("{} --install {} --altdir {} --admindir {}".format(self.alternatives_path,
                                                                           links,
                                                                           self.alt_dir,
                                                                           self.admin_dir))
        except process.CmdError as details:
            self.fail("Command failed: %s" % details)
        return True

    def alternatives_remove_all(self, name):
        try:
            process.run("{} --remove-all {} --altdir {} --admindir {}".format(self.alternatives_path,
                                                                              name,
                                                                              self.alt_dir,
                                                                              self.admin_dir))
        except process.CmdError as details:
            self.fail("Command failed: %s" % details)
        return True

