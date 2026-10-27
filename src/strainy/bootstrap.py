"""Bootstrap some dependencies on Colab."""

import os
import shutil
import subprocess
from tempfile import TemporaryDirectory
from .utils import con, download

GASPEQ_APT = [
    'apt-get', 'install', '-y', 'ncbi-blast+', 'git', 'libglpk-dev', 'r-base-core', 'bc', 'hmmer',
    'curl', 'libcurl4-openssl-dev', 'libssl-dev', 'libsbml5-dev', 'diamond-aligner', 'mmseqs2'
]

SEQKIT_URL = "https://github.com/shenwei356/seqkit/releases/download/v2.14.0/seqkit_linux_amd64.tar.gz"

def srun(cmd, check=True):
    """Run a subprocess and print the command."""
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0 and check:
        con.print(f"[bold red]Error running command:[/bold red] {' '.join(cmd)}")
        con.print(f"[bold red]Error message:[/bold red] {result.stderr}")
        raise RuntimeError(f"Command failed with return code {result.returncode}")
    return result


def r_packages(pkgs):
    """Install R packages."""
    cmd = f'install.packages(c({", ".join(["\"" + pkg + "\"" for pkg in pkgs])}))'
    return cmd


def has_gapseq():
    """Check if gapseq is installed."""
    try:
        r = srun(["gapseq", "-h"], check=False)
    except FileNotFoundError:
        return False

    status = (r.returncode < 2) & ("try to find enzymes" in r.stdout)
    return status


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

    con.print(":hammer: Installing [green]gapseq[/green] dependencies [gray][18 m][/gray].")
    srun(GASPEQ_APT)
    srun(["R", "-s", "-e", r_packages(["data.table", "stringr", "getopt", "R.utils", "stringi", "jsonlite", "httr", "pak", "getopt", "BiocManager"])])
    srun(["R", "-s", "-e", "BiocManager::install('Biostrings')"])
    srun(["R", "-s", "-e", 'pak::pkg_install("Waschina/cobrar")'])
    con.print(":hammer: Done.")
    con.print(":hammer: Installing [green]gapseq[/green] [gray][1 m][/gray].")
    srun(["git", "clone", "https://github.com/jotech/gapseq", "/usr/local/gapseq"])
    srun(["ln", "-s", "/usr/local/gapseq/gapseq", "/usr/local/bin/gapseq"])
    srun(["chmod", "+x", "/usr/local/gapseq/gapseq"])
    con.print(":hammer: Done.")
    con.print(":hammer: Installing [green]gapseq[/green] databases [gray][5 m][/gray].")
    srun(["/usr/local/gapseq/gapseq", "update-sequences", "-t", "Bacteria"])
    srun(["/usr/local/gapseq/gapseq", "update-sequences", "-t", "Archaea"])
    con.print(":hammer: Done.")


def install_seqkit():
    with TemporaryDirectory() as tmpdir:
        con.print(":hammer: Installing [green]seqkit[/green] [gray][1 m][/gray].")
        download(SEQKIT_URL, f"{tmpdir}/seqkit.tar.gz")
        srun(["tar", "-xzf", f"{tmpdir}/seqkit.tar.gz", "-C", tmpdir])
        srun(["chmod", "+x", f"{tmpdir}/seqkit"])
        srun(["mv", f"{tmpdir}/seqkit", "/usr/local/bin/seqkit"])
        con.print(":hammer: Done.")


def main():
    """Install some dependencies."""
    if am_i_colab():
        if not has_gapseq():
            install_gapseq()
        else:
            con.print(":white_check_mark: [green]gapseq[/green] is already installed.")

        install_seqkit()

        if os.path.exists("/content/sample_data"):
            shutil.rmtree("/content/sample_data")
        con.print(":hammer: All clean now.")
    else:
        con.print(
            ":fearful: This does not look like Colab, I better not touch anything."
        )
