"""Some helpers for the course."""

import gzip
import requests
import pandas as pd
import os
from pathlib import Path
import shutil
from hashlib import sha256
from tempfile import TemporaryFile, TemporaryDirectory
from rich.console import Console
import seaborn as sns

BASE = Path(".")
DATA_URL = "https://raw.githubusercontent.com/dienerlab/2026_strain_course/refs/heads/main/data/"
TREASURE_URL = "https://raw.githubusercontent.com/dienerlab/2026_strain_course/refs/heads/main/treasure_chest/"

num_genomes = 51
assemblies = pd.read_csv(
    "https://raw.githubusercontent.com/dienerlab/2026_strain_course/"
    "refs/heads/main/data/strain_manifest.csv"
)


con = Console()
secret_names = {
    "Christian Diener": 50,
    "Geoffrey Olweny": 51
}

def download_gzip(url: str, filename: str | os.PathLike[str]) -> None:
    """Download and extract a gzipped URL to a file.

    Parameters
    ----------
    url : str
        URL of the gzipped file.
    filename : str or os.PathLike[str]
        Destination path for the extracted file.

    Returns
    -------
    None
    """
    req = requests.get(url, stream=True)
    with TemporaryFile(suffix="fna.gz") as tfile:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                tfile.write(chunk)
                tfile.flush()
        tfile.seek(0)
        with gzip.open(tfile, "rb") as inf, open(filename, "wb") as outf:
            shutil.copyfileobj(inf, outf)


def download(url: str, filename: str | os.PathLike[str]) -> None:
    """Download a URL to a file.

    Parameters
    ----------
    url : str
        URL of the file to download.
    filename : str or os.PathLike[str]
        Destination path for the downloaded file.

    Returns
    -------
    None
    """
    req = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def unzip(infile: Path, outfile: Path) -> None:
    """Extract a gzip file.

    Parameters
    ----------
    infile : pathlib.Path
        Path to the gzip file.
    outfile : pathlib.Path
        Destination path for the extracted file.

    Returns
    -------
    None
    """
    with gzip.open(infile, "rb") as inf, open(outfile, "wb") as outf:
        shutil.copyfileobj(inf, outf)


def gimme_genome(name: str) -> None:
    """Download the genome assembly assigned to a course participant.

    Parameters
    ----------
    name : str
        Your name or nickname. Make it long and unique.

    Returns
    -------
    None
        Downloads the assembly and prints information about it.
    """
    if name == "[YOUR NAME]":
        con.print(
            "Ehem, I do need you to input your [bold red]name[/bold red]... "
            ":face_with_raised_eyebrow:"
        )
        return

    if not BASE.exists():
        con.print(
            "Please run this in the [bold red]materials directory[/bold red], "
            "where the data folder is located. :face_with_raised_eyebrow:"
        )

    if name not in secret_names:
        magic_number = int(sha256(name.encode()).hexdigest(), 16) % num_genomes
        con.print(
            "Hi, [bold royal_blue1]{}[/bold royal_blue1]! "
            "Welcome to the course :tada:".format(name))
    else:
        magic_number = secret_names[name]
        con.print("Oooh, you are an instructor :star-struck: Thanks for helping out!")

    os.environ["MAGIC_NUMBER"] = str(magic_number)
    assembly = assemblies.iloc[magic_number]
    aid = assembly["id"]
    os.environ["ASSEMBLY"] = aid
    taxa = assembly[["domain", "phylum", "class", "order", "family", "genus", "species", "strain"]].values

    try:
        download_gzip(DATA_URL + assembly["file"], BASE / f"{aid}.fna")
    except Exception as e:
        con.print(
            "[dark_orange]Uh oh, looks like something went wrong downloading. "
            "Just run the cell again and everything should work :smile:."
        )
        con.print(f"[dark_orange]Error message: {e}[/dark_orange]")
        return
    con.print(f"Saved the assembly to [green]{aid}.fna[/green].")
    con.print(
        f"Wow! Your assembly is [green]{aid}[/green] which is "
        f"[green]{assembly['strain']}[/green] :exploding_head: \n"
        f"By the way, the full GTDB taxonomic assignment is {' | '.join(taxa)} :nerd_face:"
    )


def gimme_abundances() -> pd.DataFrame:
    """Load the MICOM abundance table.

    Returns
    -------
    pandas.DataFrame
        Abundance data for the course strains.
    """
    return pd.read_csv(DATA_URL + "abundances.csv")


def gimme_manifest() -> pd.DataFrame:
    """Download and load the strain manifest.

    Returns
    -------
    pandas.DataFrame
        Strain manifest data.
    """
    download(DATA_URL + "strain_manifest.csv", BASE / "strain_manifest.csv")
    return pd.read_csv(BASE / "strain_manifest.csv")


def gimme_medium(format: str = "gapseq") -> pd.DataFrame:
    """Load the growth medium in the requested format.

    Parameters
    ----------
    format : str, default="gapseq"
        Output format, either ``"gapseq"`` or ``"micom"``.

    Returns
    -------
    pandas.DataFrame
        Medium composition in the requested format.

    Raises
    ------
    ValueError
        If ``format`` is not ``"gapseq"`` or ``"micom"``.
    """
    med = pd.read_csv(DATA_URL + "gut_medium_gapseq.csv")
    if format == "gapseq":
        return med
    elif format == "micom":
        med = med.rename(columns={"compounds": "metabolite", "maxFlux": "flux"})
        med["reaction"] = "EX_" + med["metabolite"] + "_m"
        return med
    else:
        raise ValueError("format must be 'gapseq' or 'micom'.")


def gimme_strain_db() -> pd.DataFrame:
    """Download and load the strain model database.

    Returns
    -------
    pandas.DataFrame
        Strain model database manifest.
    """
    from micom.db import load_zip_model_db

    download(DATA_URL + "infants_gtdb232_strain_1.zip", BASE / "infants_gtdb232_strain_1.zip")
    with TemporaryDirectory() as tmpdir:
        man = load_zip_model_db(BASE / "infants_gtdb232_strain_1.zip", tmpdir)

    return man


def gimme_treasure(file: str, compressed: bool = False) -> Path:
    """Download a file from the course treasure chest.

    Parameters
    ----------
    file : str
        Path of the file in the treasure chest.
    compressed : bool, default=False
        Whether the downloaded file is gzip-compressed.

    Returns
    -------
    pathlib.Path
        Path to the downloaded file.
    """
    out = Path(file).name
    if compressed:
        download_gzip(TREASURE_URL + file, BASE / out)
    else:
        download(TREASURE_URL + file, BASE / out)
    return BASE / out


def colormap(series: pd.Series) -> pd.Series:
    """Map each distinct string in a series to a discrete color.

    Parameters
    ----------
    series : pandas.Series of str
        Values to map to colors.

    Returns
    -------
    pandas.Series of tuple of float
        RGB color for each value, indexed like ``series``.
    """
    levels = series.unique()
    palette = sns.color_palette(n_colors=len(levels))
    cmap = pd.Series({l: palette[i] for i, l in enumerate(levels)})
    return pd.Series(cmap[series].values, index=series.index)



def add_r_squared(
    permanova_results: pd.Series,
) -> pd.Series:
    """Add the R-squared value to a PERMANOVA result.

    Parameters
    ----------
    permanova_results : pandas.Series
        Result series returned by scikit-bio's ``permanova`` function.

    Returns
    -------
    pandas.Series
        The input results with an ``"R²"`` entry added.
    """
    p = permanova_results
    r2 = 1 - 1 / (1 + p[4] * p[3] / (p[2] - p[3] - 1))
    p["R²"] = r2
    return(p)
