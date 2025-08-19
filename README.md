# MScMathematicalPhysicsEdinburgh
This repository contains simulation and analysis code used in the production of my MSc in Mathematical Physics dissertation at the University of Edinburgh.

The source code for KymoKnot and LAMMPS, both used in this work, has not been replicated. However, both are needed for the scripts here to work properly. If you intend to use these scripts, we recommend downloading and compiling the source code from their official sources. The appropriate reference to both softwares is as follows.

Tubiana L., Polles G, Orlandini E, Micheletti C. KymoKnot: A web server and software package to identify and locate knots in trajectories of linear or circular polymers. The European Physical Journal E, 41(6), 72. (2018).

LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales, A. P. Thompson, H. M. Aktulga, R. Berger, D. S. Bolintineanu, W. M. Brown, P. S. Crozier, P. J. in 't Veld, A. Kohlmeyer, S. G. Moore, T. D. Nguyen, R. Shan, M. J. Stevens, J. Tranchida, C. Trott, S. J. Plimpton, Comp Phys Comm, 271 (2022) 10817.

Any scripts involving the 'Two Hit' model also require a custom fix which can be found at git.ecdf.ed.ac.uk/s2469797/topo2-lammps. The script MakeKnotFile.cpp was taken from Davide Michieletto's LAMMPS tutorials, found at www2.ph.ed.ac.uk/~dmichiel/Lab.html.




File Structure:

--Root
    --Automation contains the 'automation script' described in the dissertation, which serves to analyse forces and, in the case of the Two Hit model, collision frequencies.
    --RampDown contains a heavily modified Automation script which is intended to track the behaviour of systems on route to equilibrium, instead of in equilibrium.
    --OneDimensionalLangevin contains the following files, all related to the One Dimensional Langevin model described in the dissertation
        --ProbabilityDistributions creates probability distributions for resetting and equilibrium cases, as displayed in the dissertation
        --DemonstrationRun produces the results of the demonstration case, except for the probability distribution figure
        --(A)SymmetricCentralPotentialRuns respectively run the symmetric and asymmetric versions of our model for a series of central potentials
