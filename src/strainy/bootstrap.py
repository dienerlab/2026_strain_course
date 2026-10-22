"""Bootstrap some dependencies on Colab."""

import os
import shutil
from subprocess import run as srun
from .utils import con

GASPEQ_APT = [
    'sudo', 'apt-get', 'install', '-y', 'install', 'ncbi-blast+', 'git', 'libglpk-dev', 'r-base-core', 'bc',
    'curl', 'libcurl4-openssl-dev', 'libssl-dev', 'libsbml5-dev', 'diamond-aligner', 'mmseqs2'
]


def am_i_colab():
    """Check if running on colab."""
    state = (
        os.path.exists("/content")
        and os.environ.get("HOME") == "/root"
        and "COLAB_JUPYTER_IP" in os.environ
        and "COLAB_IMAGE_TYPE" in os.environ
    )
    return state


def install_gapseq():
    """Install gapseq."""
    if not am_i_colab():
        con.print(
            ":fearful: This does not look like Colab, I better not touch anything."
        )

    con.print(":hammer: Installing [green]gapseq[/green] dependencies.")
    srun(GASPEQ_APT, check=True)
    srun(["R", "-e", 'install.packages(c("data.table", "stringr", "getopt", "R.utils", "stringi", "jsonlite", "httr", "pak"))'], check=True)
    srun(["R", "-e",  'if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install("Biostrings")'], check=True)
    srun(["R", "-e", 'pak::pkg_install("Waschina/cobrar")'], check=True)
    con.print(":hammer: Done.")
    con.print(":hammer: Installing [green]gapseq[/green].")
    srun(["git", "clone", "https://github.com/jotech/gapseq", "/usr/local/gapseq"], check=True)
    srun(["ln", "-s", "/usr/local/gapseq/gapseq", "/usr/local/bin/gapseq"], check=True)
    srun(["chmod", "+x", "/usr/local/gapseq/gapseq"], check=True)
    con.print(":hammer: Done.")
    con.print(":hammer: Installing [green]gapseq[/green] databases.")
    srun(["/usr/local/gapseq/gapseq", "update-sequences", "-t", "Bacteria"], check=True)
    srun(["/usr/local/gapseq/gapseq", "update-sequences", "-t", "Archaea"], check=True)
    con.print(":hammer: Done.")


def main():
    """Install some dependencies."""
    if am_i_colab():
        install_gapseq()
        if os.path.exists("/content/sample_data"):
            shutil.rmtree("/content/sample_data")
        con.print(":hammer: All clean now.")
    else:
        con.print(
            ":fearful: This does not look like Colab, I better not touch anything."
        )
