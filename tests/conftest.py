import os
import sys

# The repo root, so `hpc.ledger` imports without installing anything.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# The eccodes bindings need the gcc-12 libstdc++ and the spack eccodes library,
# which tools/eccodes_env.sh provides through LD_PRELOAD for interactive use.
# LD_PRELOAD cannot be set from inside a running process, but loading the same
# libstdc++ with RTLD_GLOBAL before the first `import eccodes` has the same
# effect, so a plain `uv run pytest` can read and write GRIB. The paths are read
# from that script, so there is still one place that names them.
def _eccodes_from_env_script():
    import ctypes
    import re
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          'tools', 'eccodes_env.sh')
    try:
        text = open(script).read()
    except OSError:
        return
    paths = dict(re.findall(r'^(GCC12_RT|ECCODES_LIB)="([^"]+)"', text, re.M))
    stdcxx = os.path.join(paths.get('GCC12_RT', ''), 'libstdc++.so.6')
    if 'ECCODES_LIB' not in paths or not os.path.isfile(stdcxx):
        return
    ctypes.CDLL(stdcxx, mode=ctypes.RTLD_GLOBAL)
    os.environ.setdefault('ECCODES_DIR', os.path.dirname(paths['ECCODES_LIB']))


_eccodes_from_env_script()
