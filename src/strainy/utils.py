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

def download_gzip(url, filename):
    """Download and extract a gzipped URL to a file."""
    req = requests.get(url, stream=True)
    with TemporaryFile(suffix="fna.gz") as tfile:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                tfile.write(chunk)
                tfile.flush()
        tfile.seek(0)
        with gzip.open(tfile, "rb") as inf, open(filename, "wb") as outf:
            shutil.copyfileobj(inf, outf)


def download(url, filename):
    """Download URL to a file."""
    req = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()


def unzip(infile : Path, outfile : Path):
    """Download and extract a gzipped URL to a file."""
    with gzip.open(infile, "rb") as inf, open(outfile, "wb") as outf:
        shutil.copyfileobj(inf, outf)


def gimme_genome(name : str):
    """Return a genome for the given name.

    Arguments
    ---------
    name : str
        Your name or nickname. Make it long and unique.

    Returns
    -------
    Nothing, but prints a lot of info and downloads your genome assembly.

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


def gimme_abundances():
    """Return a MICOM abundance table."""
    return pd.read_csv(DATA_URL + "abundances.csv")


def gimme_manifest():
    """Return the strain manifest."""
    download(DATA_URL + "strain_manifest.csv", BASE / "strain_manifest.csv")
    return pd.read_csv(BASE / "strain_manifest.csv")


def gimme_medium(format="gapseq"):
    """Return the medium."""
    med = pd.read_csv(DATA_URL + "gut_medium_gapseq.csv")
    if format == "gapseq":
        return med
    elif format == "micom":
        med = med.rename(columns={"compounds": "metabolite", "maxFlux": "flux"})
        med["reaction"] = "EX_" + med["metabolite"] + "_m"
        return med
    else:
        raise ValueError("format must be 'gapseq' or 'micom'.")


def gimme_strain_db():
    """Return the strain database."""
    from micom.db import load_zip_model_db

    download(DATA_URL + "data/infants_gtdb232_strain_1.zip", BASE / "infants_gtdb232_strain_1.zip")
    with TemporaryDirectory() as tmpdir:
        man = load_zip_model_db(BASE / "infants_gtdb232_strain_1.zip", tmpdir)

    return man


def colormap(series : pd.Series):
    """Build a discrete colormap for a bunch of strings."""
    levels = series.unique()
    palette = sns.color_palette(n_colors=len(levels))
    cmap = pd.Series({l: palette[i] for i, l in enumerate(levels)})
    return pd.Series(cmap[series].values, index=series.index)



def add_r_squared(permanova_results):
    """Get the R2 for a PERMANOVA result."""
    p = permanova_results
    r2 = 1 - 1 / (1 + p[4] * p[3] / (p[2] - p[3] - 1))
    p["R²"] = r2
    return(p)
