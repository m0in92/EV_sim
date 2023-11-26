from django.shortcuts import render
from django.http import JsonResponse

from.forms import SimulationInputForm
import EV_sim
from EV_sim.sol import Solution


def index(request):
    result_t: list = []  # intended for simulation result, initialized as empty list
    result_demand: list = []  # intended for simulation result, initialized as empty list
    result_current: list = []  # intended for simulation result, initialized as empty list
    if request.method == "POST":
        form = SimulationInputForm(request.POST)
        if form.is_valid():
            input_ev_alias, \
            input_drive_cycle, \
            input_air_density, \
            input_road_grade = get_simulation_inputs_from_post(request=request)
            print(get_simulation_inputs_from_post(request))
            obj_ev = EV_sim.EVFromDatabase(alias_name=input_ev_alias)
            obj_drive_cycle = EV_sim.DriveCycle(drive_cycle_name=input_drive_cycle)
            obj_ext_cond = EV_sim.ExternalConditions(rho=input_air_density, road_grade=input_road_grade)
            model = EV_sim.VehicleDynamics(ev_obj=obj_ev, drive_cycle_obj=obj_drive_cycle,
                                           external_condition_obj=obj_ext_cond)
            sol: Solution = model.simulate()
            result_t = sol.t.tolist()
            result_demand = sol.demand_power.tolist()
            result_current = sol.current.tolist()
    else:
        form = SimulationInputForm()

    return render(request=request, template_name='index.html', context={'form': form,
                                                                        't': result_t,
                                                                        'demand': result_demand,
                                                                        'current': result_current})

def get_simulation_inputs_from_post(request) -> tuple[str, str, float, float]:
    request_post = request.POST
    return (request_post['ev_alias'], request_post['drive_cycle'],
            float(request_post['air_density']), float(request_post['road_grade']))

