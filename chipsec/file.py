# CHIPSEC: Platform Security Assessment Framework
# Copyright (c) 2010-2021, Intel Corporation
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; Version 2.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Contact information:
# chipsec@intel.com
#


#
# -------------------------------------------------------------------------------
#
# CHIPSEC: Platform Hardware Security Assessment Framework
# (c) 2010-2012 Intel Corporation
#
# -------------------------------------------------------------------------------

"""
Reading from/writing to files

usage:
    >>> read_file(filename)
    >>> write_file(filename, buffer)
"""

import sys
import os

from typing import Any
from chipsec.logger import logger

TOOLS_DIR = 'chipsec_tools'


def read_file(filename: str, size: int = 0) -> bytes:
    try:
        f = open(filename, 'rb')
    except:
        logger().log_error(f"Unable to open file '{filename:.256}' for read access")
        return b''

    if size:
        _file = f.read(size)
    else:
        _file = f.read()
    f.close()

    logger().log_debug(f"[file] Read {len(_file):d} bytes from '{filename:256}'")
    return _file


def write_file(filename: str, buffer: Any, append: bool = False) -> bool:
    perm = 'a' if append else 'w'
    if isinstance(buffer, bytes) or isinstance(buffer, bytearray):
        perm += 'b'
    try:
        f = open(filename, perm)
    except:
        logger().log_error(f"Unable to open file '{filename:.256}' for write access")
        return False
    f.write(buffer)
    f.close()

    logger().log_debug(f"[file] Wrote {len(buffer):d} bytes to '{filename:.256}'")
    return True


# determine if CHIPSEC is loaded as chipsec.exe or in python
def main_is_frozen() -> bool:
    return (hasattr(sys, "frozen") or  # new py2exe
            hasattr(sys, "importers"))  # old py2exe


def get_main_dir() -> str:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
    if main_is_frozen():
        path = os.path.dirname(sys.executable)
    return path
