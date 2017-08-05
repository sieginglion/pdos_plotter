from pymatgen.io.vasp.outputs import Vasprun
from numpy import array
import matplotlib.pyplot as pp

vasprun = Vasprun('vasprun.xml', parse_dos = True)
pdos = vasprun.complete_dos.pdos
efermi = vasprun.complete_dos.efermi
energies = list(vasprun.complete_dos.energies)

def merger():
    merged = {}
    for site in pdos:
        data = pdos[site]
        site = str(site)
        atom = site[site.index(']') + 2:]
        up, down = array([0.0 for i in range(len(energies))]), array([0.0 for i in range(len(energies))])
        for orbital in data.values():
            items = list(orbital.items())
            for item in items:
                if int(item[0]) == 1:
                    up += item[1]
                else:
                    down -= item[1]
        if atom not in merged.keys():
            merged[atom] = [up, down]
        else:
            merged[atom][0] += up
            merged[atom][1] += down
    return merged

def plotter(spin_up, spin_down, atoms):
    merged = merger()
    for atom in atoms:
        up = merged[atom][0]
        down = merged[atom][1]
        if spin_up == True:
            pp.plot(energies, up, label = atom)
        if spin_down == True:
            pp.plot(energies, down, label = atom)
    if spin_up == True:
        pp.plot([efermi, efermi], [0, 5], linestyle = '--', color = 'k')
    if spin_down == True:
        pp.plot([efermi, efermi], [0, -5], linestyle = '--', color = 'k')
    zeros = [0 for i in range(len(energies))]
    pp.plot(energies, zeros, linestyle = '--', color = 'k')
    pp.legend()
    pp.show()

# Example: plotter(spin_up = True, spin_down = False, atoms = ['Mo', 'S'])