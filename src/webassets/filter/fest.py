from __future__ import with_statement

import os
import subprocess

from webassets.exceptions import FilterError
from webassets.filter import Filter


class Fest(Filter):
    """
    Asset filter for fest templates.
    """
    name = 'fest'
    options = {
        'fest': ('binary', 'FEST_COMPILE_BIN'),
        'fest_template_dir': 'FEST_TEMPLATE_DIR'
    }
    max_debug_level = None

    def _compile_fest(self, source_path, out):
        """
        Compile fest template.
        """
        old_dir = os.getcwd()
        os.chdir(self.fest_template_dir)

        try:
            args = [
                self.fest or 'fest-compile',
                source_path,
            ]

            proc = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = proc.communicate()

            if proc.returncode != 0:
                raise FilterError(
                    'fest: subprocess had error: stderr=%s, '
                    'stdout=%s, returncode=%s'
                    % (stderr, stdout, proc.returncode)
                )
            elif stderr:
                print "fest filter has warnings:", stderr

            out.write(stdout)
        finally:
            os.chdir(old_dir)

    def input(self, _in, out, source_path, **kwargs):
        """
        Input fest template.
        Called for every source file.
        """
        if source_path.endswith('.xml'):
            self._compile_fest(source_path, out)
        else:
            out.write(_in.read())
