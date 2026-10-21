"""Some helpers for the course."""

import gzip
import pandas as pd
import os
from pathlib import Path
import shutil
from hashlib import sha256
from rich.console import Console
import seaborn as sns

BASE = Path("/content/materials/")

num_genomes = 51
assemblies = pd.read_csv(BASE / "strain_manifest.csv")

prefix_map = pd.Series({
    "d": "domain",
    "p": "phylum",
    "c": "class",
    "o": "order",
    "f": "family",
    "g": "genus",
    "s": "species"
})
con = Console()
secret_names = {
    "Christian Diener": 50,
    "Geoffrey Olweny": 51
}


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
        unzip(BASE / Path(assembly["file"]), BASE / f"{aid}.fna")
    except Exception:
        con.print(
            "[dark_orange]Uh oh, looks like something went wrong downloading. "
            "Just run the cell again and everything should work :smile:."
        )
        return
    con.print(f"Saved the assembly to [green]{{aid}}.fna[/green].")
    con.print(
        f"Wow! Your assembly is [green]{aid}[/green] which is "
        f"[green]{assembly['strain']}[/green] :exploding_head: \n"
        f"By the way, the full GTDB taxonomic assignment is {' | '.join(taxa)} :nerd_face:"
    )
    return aid


def gimme_abundances():
    """Return a MICOM abundance table."""
    return pd.read_csv(BASE / "abundances.csv")


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
