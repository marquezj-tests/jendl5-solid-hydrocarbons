jendl5-solid-hydrocarbons: NCrystal data plugin
===============================================

NCrystal data-only plugin (based on the `DummyDataPlugin` example in the NCrystal repository,
`examples/plugin_dataonly`) providing NCMAT files for the solid hydrocarbons of the JENDL-5 thermal scattering
sublibrary (TSL) evaluated at Kyoto University (`KYOTO-U`, EVAL-FEB21, Y. Abe). Companion of
[jendl5-liquids](https://github.com/marquezj-tests/jendl5-liquids).

One file per material and temperature, named `<material>_solid_<T>K.ncmat`, referenced in NCrystal as
`plugins::jendl5-solid-hydrocarbons/<file>` (22 files):

| Material | ENDF-6 files (JENDL-5 TSL) | Temperatures [K] |
|---|---|---|
| ethanol (C2H6O) | H(C2H6O)_0607, C(C2H6O)_0637, O(C2H6O)_0667 | 20, 100 |
| benzene (C6H6) | H(C6H6)_0611, C(C6H6)_0641 | 20, 50, 100, 150 |
| toluene (C7H8) | H(C7H8)_0042, C(C7H8)_0642 | 20, 50, 100, 150 |
| mesitylene (C9H12) | H(C9H12)_0038, C(C9H12)_0638 | 20, 50, 100, 150 |
| m-xylene (C8H10) | H(m-C8H10)_0613, C(m-C8H10)_0643 | 20, 50, 100, 150 |
| methane (CH4) | H(CH4)_0034, C(CH4)_0634 | 20 |
| triphenylmethane (C19H16) | H(C19H16)_0615, C(C19H16)_0645 | 20, 100, 300 |

Not included: polyethylene and Lucite (evaluated at LEIP LAB, not Kyoto), and the liquid phases (see jendl5-liquids).

Notes and limitations
---------------------

* Files were generated with `NCMATComposer.set_dyninfo_scatknl` from the ENDF-6 MF7/MT4 data of each atom, combining the
  per-atom files of one molecule into one NCMAT file.
* **Only the inelastic part of the evaluation is present.** The ENDF-6 files also give an incoherent elastic component
  (MT2) for these solids; it is not in the NCMAT files, so total scattering at low energy is underestimated. Elastic
  scattering can be added by the user.
* Densities are nominal values chosen by the converter, not taken from ENDF-6.
* ENDF-6 S(alpha,beta) grids are rescaled to NCMAT conventions (LAT=1 scaling, ln S converted to S).
* Against NJOY2016 thermr (inelastic only) every file agrees at 0.0253 eV within 0.03% and over 1e-5 eV to 10 eV with an
  RMS deviation of 0.1-0.9% (largest at the lowest temperature, 20 K). See `plots/summary.csv`.

Usage
-----

    pip install ./jendl5-solid-hydrocarbons
    ncrystal-inspect plugins::jendl5-solid-hydrocarbons/benzene_solid_20K.ncmat

NCrystal discovers installed plugins through `ncrystal-pluginmanager`. Plugin data files are only served on explicit
request, hence the `plugins::` prefix. Use `ncrystal-config --browse` or `NCrystal.browseFiles()` to list the files.

Repository layout
-----------------

* `src/ncrystal_plugin_jendl5-solid-hydrocarbons/` - the plugin (python package and `data/` with the NCMAT files). Only this
  directory is packaged.
* `reference/` - NJOY2016 thermr inelastic cross sections (one CSV per NCMAT file, per-atom average over the molecule).
  `reference/effective_temperature.csv` lists the effective temperature T_eff [K] of the principal scatterer, from the ENDF-6
  MF7/MT4 table of each source file, for every material, temperature and atom type of the plugin.
* `scripts/compare_with_reference.py` - loads the installed plugin files with NCrystal and plots them against `reference/`
  (`python scripts/compare_with_reference.py [--out DIR] [pattern ...]`).
* `plots/` - NCrystal vs NJOY comparison plot for each file, and `summary.csv`.
