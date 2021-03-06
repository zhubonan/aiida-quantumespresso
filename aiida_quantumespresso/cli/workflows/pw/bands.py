# -*- coding: utf-8 -*-
import click
from aiida_quantumespresso.utils.click import command
from aiida_quantumespresso.utils.click import options


@command()
@options.code()
@options.structure()
@options.pseudo_family()
@options.kpoint_mesh()
@options.max_num_machines()
@options.max_wallclock_seconds()
@options.daemon()
@options.automatic_parallelization()
def launch(
    code, structure, pseudo_family, kpoints, max_num_machines, max_wallclock_seconds, daemon,
    automatic_parallelization):
    """
    Run the PwBandsWorkChain for a given input structure
    """
    from aiida.orm.data.base import Bool, Float, Str
    from aiida.orm.data.parameter import ParameterData
    from aiida.orm.utils import WorkflowFactory
    from aiida.work.run import run, submit
    from aiida_quantumespresso.utils.resources import get_default_options

    PwBandsWorkChain = WorkflowFactory('quantumespresso.pw.bands')

    parameters = {
        'SYSTEM': {
            'ecutwfc': 30.,
            'ecutrho': 240.,
        },
    }

    relax_inputs = {
        'kpoints_distance': Float(0.2),
        'parameters': ParameterData(dict=parameters),
    }

    inputs = {
        'code': code,
        'structure': structure,
        'pseudo_family': Str(pseudo_family),
        'kpoints': kpoints,
        'parameters': ParameterData(dict=parameters),
        'relax': relax_inputs,
    }

    if automatic_parallelization:
        parallelization = {
            'max_num_machines': max_num_machines,
            'target_time_seconds': 0.5 * max_wallclock_seconds,
            'max_wallclock_seconds': max_wallclock_seconds
        }
        inputs['automatic_parallelization'] = ParameterData(dict=parallelization)
    else:
        options = get_default_options(max_num_machines, max_wallclock_seconds)
        inputs['options'] = ParameterData(dict=options)

    if daemon:
        workchain = submit(PwBandsWorkChain, **inputs)
        click.echo('Submitted {}<{}> to the daemon'.format(PwBandsWorkChain.__name__, workchain.pid))
    else:
        run(PwBandsWorkChain, **inputs)
