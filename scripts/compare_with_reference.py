"""Load NCMAT files of the installed jendl5-solid-hydrocarbons plugin and plot their inelastic cross section against the NJOY2016
reference data in ../reference.

Usage: python compare_with_reference.py [--out DIR] [--ref DIR] [pattern ...]
Each pattern is a substring of an ncmat file name (default: all files of the plugin that have reference data).
Requires: NCrystal, the installed plugin (pip install .), numpy, matplotlib.
"""
import os, sys, argparse, csv
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import NCrystal as NC

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = 'jendl5-solid-hydrocarbons'

def read_reference(path):
    d = np.loadtxt(path, delimiter=',', skiprows=4)
    return np.ascontiguousarray(d[:, 0]), np.ascontiguousarray(d[:, 1])   # NCrystal's array calls need contiguous input

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('patterns', nargs='*')
    ap.add_argument('--ref', default=os.path.join(HERE, '..', 'reference')); ap.add_argument('--out', default='ncrystal_vs_njoy')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); rows = []
    names = sorted(f[:-len('_njoy.csv')] for f in os.listdir(a.ref) if f.endswith('_njoy.csv'))
    for stem in names:
        for variant in (stem, stem + '_refined_grid'):
            key = f'plugins::{PLUGIN}/{variant}.ncmat'
            if a.patterns and not any(p in variant for p in a.patterns): continue
            try: sc = NC.createScatter(key)
            except NC.NCException as e:
                if variant == stem:   # only some files have a _refined_grid variant
                    print(f'WARNING: could not load {key} (is the plugin installed?): {e}', file=sys.stderr)
                continue
            E, ref = read_reference(os.path.join(a.ref, stem + '_njoy.csv'))
            xs = np.asarray(sc.crossSectionIsotropic(E)); r = xs / ref
            rows.append(dict(file=variant, ratio_0p0253=float(np.interp(0.0253, E, r)), ratio_min=float(r.min()), ratio_max=float(r.max()),
                             rms_rel_dev=float(np.sqrt(np.mean((r - 1) ** 2)))))
            fig, (ax, ar) = plt.subplots(2, 1, figsize=(6.5, 5.5), sharex=True, gridspec_kw=dict(height_ratios=[3, 1.3]))
            ax.loglog(E, ref, 'k--', label='NJOY thermr (reference)'); ax.loglog(E, xs, label='NCrystal ' + variant)
            ax.set_ylabel('Inelastic xs [b/atom]'); ax.legend(fontsize=7); ax.grid(alpha=.3, which='both')
            ar.semilogx(E, r); ar.axhline(1, color='k', lw=.5); ar.set_ylabel('NCrystal / NJOY'); ar.set_xlabel('Neutron energy [eV]'); ar.grid(alpha=.3)
            fig.tight_layout(); fig.savefig(os.path.join(a.out, variant + '.png'), dpi=90); plt.close(fig)
            print(f"{variant}: ratio(0.0253 eV)={rows[-1]['ratio_0p0253']:.4f} rms={rows[-1]['rms_rel_dev']:.4f}", flush=True)
    if rows:
        with open(os.path.join(a.out, 'summary.csv'), 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    main()
