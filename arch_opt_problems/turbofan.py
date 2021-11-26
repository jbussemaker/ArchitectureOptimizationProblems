"""
Licensed under the GNU General Public License, Version 3.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.gnu.org/licenses/gpl-3.0.html.en

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Copyright: (c) 2021, Deutsches Zentrum fuer Luft- und Raumfahrt e.V.
Contact: jasper.bussemaker@dlr.de
"""

import os
os.environ['OPENMDAO_REQUIRE_MPI'] = 'false'

__all__ = ['get_turbofan_problem']


def get_turbofan_problem(par_pool=None):
    from open_turb_arch.architecting.architecting_problem import \
        get_architecting_problem, get_pymoo_architecting_problem
    return get_pymoo_architecting_problem(get_architecting_problem(), parallel_pool=par_pool)


if __name__ == '__main__':
    # from pymoo.indicators.hv import Hypervolume
    # pf = get_turbofan_problem().pareto_front()
    # print(Hypervolume(pf=pf, normalize=True).calc(pf))

    from arch_opt_problems.discretization import print_sparseness
    print_sparseness(get_turbofan_problem(), n_samples=10000, n_cont=6), exit()

    import multiprocessing
    from pymoo.optimize import minimize
    from pymoo.algorithms.moo.nsga2 import NSGA2
    with multiprocessing.Pool() as pool:
        problem = get_turbofan_problem(pool)
        algo = NSGA2(pop_size=5)
        minimize(problem, algo, termination=('n_eval', 20))
