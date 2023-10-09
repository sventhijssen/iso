import pathlib
import platform

from cli.ContextManager import ContextManager
from aux.Log import Log

context_manager = ContextManager()
log = Log()

# Settings for BDD
time_limit_bdd = 3600

# For equivalence checking
record_formulae = False
equivalence_checker_timeout = 3600

root = pathlib.Path(__file__).parent.parent.parent.absolute()
benchmark_path = root.joinpath('benchmarks')
abc_path = root.joinpath('abc')

if platform.system() == 'Windows':
    bash_cmd = ['bash', '-c']
elif platform.system() == 'Linux':
    bash_cmd = ['/bin/bash', '-c']
elif platform.system() == 'Darwin':
    bash_cmd = ['/bin/bash', '-c']
else:
    raise Exception("Unsupported OS: {}".format(platform.system()))

abc_cmd = bash_cmd.copy()
abc_cmd.extend(['"./abc"'])
abc_cmd = ' '.join(abc_cmd)
