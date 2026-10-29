![header](docs/reconstruction/assets/mm_course_2026.png)

# Materials and Slides

This repository contains the materials and slides for the course `Strain-level metabolic modeling of microbial communities`. It generally consists of four parts

1. A course Python package that manages the installation of additional dependencies and getting data for the course.
2. Data and cached output ("treasure chest") for the course.
3. Interactive slides.
4. Google Colab Notebook that give hands-on training.

## The strainy package

This helper package should only be installed on Colab.

```bash
pip install git+https://github.com/dienerlab/2026_strain_level_course
```

This exposes several helper functions usually called `gimme_*` to download specific data sets. It also provides a `bootstrap` command that installs GAPSEQ and SEQKIT.

## Part 1: From Genome to Model & Part 2: From Model to Fluxes

[Slides](https://dienerlab.github.io/2026_strain_course/reconstruction) - [Notebook](https://colab.research.google.com/github/dienerlab/2026_strain_course/blob/main/reconstruction.ipynb)

## Part 3: From Models to Communities

[Slides](https://dienerlab.github.io/2026_strain_course/micom) - [Notebook](https://colab.research.google.com/github/dienerlab/2026_strain_course/blob/main/micom.ipynb)

## Emergency plan: the treasure chest

For long running scripts we provide cached results that can be downloaded within the Colab notebooks. This is exposed
through the `gimme_treasure` function in `strainy`. Just pick any file or sub-path within the [treasure_chest](/treasure_chest) folder of the respoitory.

```python
from strainy import gimme_treasure

gimme_treasure("growth.zip")

# In subfolder, will also unzip the file
gimme_treasure("gapseq/GCA_000010425.1.xml.gz", compressed=True)
```