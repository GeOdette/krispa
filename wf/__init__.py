"""
Reconstruct CRIPR locus from a M.tb complex genome
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile


@small_task
def CRISPRbuilder_TB_task(SRA_reference: str):
    cs_ex = Path("crsptb.txt").resolve()

    _CRISPRbuilder_TB = [
        "python",
        "-m",
        "crisprbuilder_tb",
        "--collect",
        str(SRA_reference),
    ]
    subprocess.run(_CRISPRbuilder_TB, check=True)
    return LatchFile(str(cs_ex), "latch:///crsptb.txt")


@ workflow
def krispa(SRA_reference: str):
    """Reconstruct CRIPR locus from a M.tb complex genome


     __metadata__:
         display_name: Assemble and Sort FastQ Files
         author:
             name:
             email:
             github:
         repository:
         license:
             id: MIT

     Args:

         SRA_reference:
           Input SRA_reference number e.g SRR1173284

           __metadata__:
             display_name: SRA reference number
     """
    return CRISPRbuilder_TB_task(SRA_reference=SRA_reference)


# if __name__ == "__main__":
# krispa(SRA_reference=str("SRR11192680"))
