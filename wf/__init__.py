"""
collect and annotate Mycobacterium tuberculosis whole genome sequencing data for CRISPR investigation
"""

import subprocess
from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile, LatchDir
from typing import Optional
import os


@small_task
def CRISPRbuilder_TB_task(SRA_reference: Optional[str],
                          list: Optional[LatchFile],
                          output_dir: LatchDir,
                          print_lineage: bool = False,
                          multiple_SRA: bool = False,
                          collect: bool = False) -> LatchDir:

    # Define path to the list of SRA refs and check if file exists
    if multiple_SRA == True & os.path.exists(list.local_path):
        if Path(list).suffix == '.txt':
            _CRISPRbuilder_TB = [
                "python",
                "-m",
                "crisprbuilder_tb",
                "--list",
                list.loacal_path, ]

    if print_lineage == True:
        _CRISPRbuilder_TB = [
            "python",
            "-m",
            "crisprbuilder_tb"
            "--print",
            "0", ]

    if collect == True:
        _CRISPRbuilder_TB = [
            "python",
            "-m",
            "crisprbuilder_tb",
            "--collect",
            str(SRA_reference),
        ]

    # Defining outputs
    local_dir = Path("crspr_out")

    subprocess.run(_CRISPRbuilder_TB, check=True)
    return LatchDir(local_dir, output_dir.remote_path)


@ workflow
def krispa(SRA_reference: Optional[str],
           list: Optional[LatchFile],
           output_dir: LatchDir,
           print_lineage: bool = False,
           multiple_SRA: bool = False,
           collect: bool = False) -> LatchDir:
    """Collect and annotate Mycobacterium tuberculosis whole genome sequencing data

    # krispa

    This workflow implements the CRISPRbuilder_TB tool for collect and annotate Mycobacterium tuberculosis 

    whole genome sequencing data for CRISPR investigations

    With an input of Sequence Read Archive reference, one can obtain:

    ## Reads

    > Number of reads for the study, length of those reads, coverage of the study

    ## The study

    > Details of the study for the discoveries

    ## Identity

    > Name of the SRA reference, strain for the SRA, taxid, bioproject number

    ## Spoligotypes

    ## Lineages 

    # Basic Usaage: 
              - Ensure to have a strong connection, otherwise the workflow might fail with an erro status

    > Enter a valid SRA reference at the [Latch console](https://console.latch.bio/explore/60576/info)

    > If you have a list of SRA references, input them in a text file and activate the __list__ option

    > With appropriate inputs, click the __launch button__


    __metadata__:
         display_name: Collect and annotate Mycobacterium tuberculosis whole genome sequencing data for CRISPR investigations
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

        multiple_SRA:
          Check this if you have text containing multipple SRA

           __metadata__:
            display_name: Multipple SRA Refs

        collect:
           Check this if you want to collect information about a SRA reference

           __metadata__:
            display_name: Collect SRA reference info

        list:
           Input .txt file containing list of SRA references

           __metadata__:
            display_name: Text file containing SRA Refs


        output_dir:
           Where you want the files to be stored. *Tip: Create a directory in the Latch console

           __metadata__:
            display_name: Output Directory

        print_lineage:
           Check this if you want to rint the database lineage.csv

           __metadata__:
            display_name: Print database lineage.csv

     """
    return CRISPRbuilder_TB_task(SRA_reference=SRA_reference,
                                 list=list,
                                 output_dir=output_dir,
                                 print_lineage=print_lineage,
                                 multiple_SRA=multiple_SRA,
                                 collect=collect,)
