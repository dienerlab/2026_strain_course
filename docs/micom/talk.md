<!-- .slide: data-background="assets/backdrop.webp" class="dark" -->

## Strain-level metabolic modeling of microbial communities

# Part 3: From model to fluxes

### Christian Diener

<img src="assets/meduni/logo_slogan_dark.png" width="30%">

from the *2026 Theodor Escherich Symposium*

<br><br>
<div class="footer">
<a href="https://creativecommons.org/licenses/by-sa/4.0/"><i class="fa-solid fa-camera-retro"></i>internal</a>
<a href="https://dienerlab.com"><i class="fa-solid fa-house-signal"></i></i>dienerlab.com</a>
<a href="https://github.com/dienerlab"><i class="fa-brands fa-github"></i>dienerlab</a>
<a href="https://bsky.app/profile/cdiener.com"><i class="fa-brands fa-bluesky"></i></i>@cdiener.com</a>
</div>

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

Let's get the slides first (use your computer, phone, TV, fridge)

*https://dienerlab.github.io/2026_strain_course/micom*


---

## A Complex System

<div style="display: flex; align-items: center; justify-content: space-around">

<div style="width: 40%">

<img src="assets/motivation.svg" width="100%">

</div>

<div style="width: 50%">

The intestinal metabolic environment is an *emergent property* of microbial, dietary and host interactions each consuming *and* providing specific metabolites.

Microbial metabolite production can impact the host, e.g.
- SCFA → colonoctye interactions
- bile acids → FXR/TGR5,
- pro- and anti-inflammatory compounds
- hepatic metabolism

How much of this can we glean from *genomic* data?

</div>

</div>

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

## Do we know enough of the rules to play the game?

<br><br>

Explaining the behavior of microbial communities through mechanisms by using *flux balance analysis (FBA)*.

---

## Our dataset

<img src="assets/paper.png" width="100%">

<div class="footnote">

Baumann-Dudenhoeffer AM, D’Souza AW, Tarr PI, Warner BB, Dantas G. Infant diet and maternal gestational weight gain predict early metabolic maturation of gut microbiomes. Nat Med. 2018;24: 1822–1829. https://doi.org/10.1038/s41591-018-0216-2

</div>

---

<img src="assets/relab_infants.png" width="100%">

- 8 infants (4 vaginal birth, 4 cesarean)
- different age groups and diets
- 51 strains across the 8 infants (account for ~50% of abundance)

*Are there differences in metabolic functions across infants?*

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

## Quick reminder :clock:

<img src="assets/materials.png" width="80%">

<br>

<a href="https://colab.research.google.com/github/dienerlab/2026_strain_course/blob/main/micom.ipynb"
   target="_blank">Click me to open the notebook!</a>

---

## Genome-scale metabolic models - pretty well-behaved

<img src="assets/gsmm.webp" width="100%">

<div class="footnote">

Schuetz et al. 2012, https://doi.org/10.1126/science.1216882<br>
Harcombe et al. 2013, https://doi.org/10.1371/journal.pcbi.1003091

</div>

---

## Community-scale metabolic models - pretty rowdy

<img src="assets/csmm.webp" width="100%">

<div class="footnote">

Diener et al. 2023, https://doi.org/10.1128/msystems.01270-22

</div>

----

## They are also big...

<img src="assets/model_gephi.png" width="70%">

Genus-level metabolic model for the gut microbiome of a single individual.

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

## Let's switch to the notebook

We know how to build a community model now. Let's get started with that...

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

## Uh-oh...

So there is a well-defined community growth rate $\mu_C = \sum_i \alpha_i\mu_i$ but it does not need to be at its maximum.

And even *if* we knew $\mu_C$ this does not identify unique taxon-specific growth rates $\mu_i$.

Just *great*, really :angry:

<br>

We need a way to identify the growth rates $\mu_i$.

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

# Let's switch to the notebook

Okay, that is all just too much. Let *future me* handle this...

---

## It's all just cones

<img src="assets/growth_cone.png" width="60%">

---

<img src="assets/cones.gif" width="50%" class="centered">

---

## How to pick solutions from the growth cone

<img src="assets/strategies.webp" width="80%">

---

## Properties of ctFBA

ctFBA has some properties which intuitively make sense.

1. An organism with non-zero abundance will receive a *non-zero growth rate* if the environment allows it.
2. <i>Within a single sample</i> higher growth rate *leads to higher abundance*.
3. Most common ecological interaction is *competition*.

---

<img src="assets/micom_quick.png" width="100%">

That makes full community-scale metabolic models *usable*.

But even curated metabolic models for many species do not capture the full complexity of
metabolism. So are those models also *useful*?

How do we *validate* the model predictions?

---

## Is it better than the status quo?

<img src="assets/validation.png" width="100%">

186 metagenome samples from Swedish and Danish individuals.<br>
Manually curated metabolic models from the AGORA database.<br>
Import fluxes based on an average European diet.

<div class="footnote">

Diener et al. 2020, https://doi.org/10.1128/mSystems.00606-19<br>
Korem, Suez, Zeevi, Weinberger et al. 2015, https://dx.doi.org/10.1126%2Fscience.aac4812<br>
Magnúsdóttir et al., https://doi.org/10.1038/nbt.3703
</div>

---

<img src="assets/validation2.png" width="100%">

<div class="footnote">

Quinn-Bohmann et al. 2024, https://doi.org/10.1038/s41564-024-01728-4<br>
Carr et al. 2025, https://doi.org/10.1016/j.cels.2025.101367<br>
Quinn-Bohmann et al. 2026, https://doi.org/10.1371/journal.pbio.3003638

</div>

---

## Limitations

- steady state assumption: can not *really* model abundance changes
- hard to link with (relative) concentration data (for instance metabolomics)
- limited by GSMM quality, many enzymes/metabolites not identified (bias towards CCM)
- can only model growth-associated processes (no toxicity or secondary metabolism)

---

## Your turn

Let's get our results and see what we can learn.

<img src="assets/coding.gif" width="50%">

---

<!-- .slide: data-background="var(--primary)" class="dark" -->

# Thanks :smile:

Any open questions?

<div style="display: flex; align-items: center; justify-content: space-evenly">

<div style="width: 40%">

**MedUni Graz**<br>
Geoffrey Olweny<br>
Vanessa Csitkovics<br>
Christine Moissl-Eichinger


</div><div style="width: 50%">

**Funding**<br><br>
<img src="assets/coe_logo_white.svg" width="50%">
<img src="assets/meduni/logo_dark.png" width="20%">

</div></div>
