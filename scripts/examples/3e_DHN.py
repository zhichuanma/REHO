from reho.model.reho import *
from reho.plotting import plotting


if __name__ == '__main__':

    # Set building parameters
    reader = QBuildingsReader()
    reader.establish_connection('Geneva')
    qbuildings_data = reader.read_db(transformer=234, nb_buildings=4)

    # Select clustering options for weather data
    cluster = {'Location': 'Geneva', 'Attributes': ['T', 'I', 'W'], 'Periods': 10, 'PeriodDuration': 24}

    # Set scenario
    scenario = dict()
    scenario['Objective'] = 'TOTEX'
    scenario['name'] = 'totex'
    scenario['exclude_units'] = ['Battery', 'NG_Cogeneration']
    scenario['enforce_units'] = ['HeatPump_DHN']
    scenario["specific"] = ["enforce_DHN"]
    # Initialize available units and grids
    grids = infrastructure.initialize_grids({'Electricity': {},
                                             'NaturalGas': {},
                                             'Heat': {}})
    units = infrastructure.initialize_units(scenario, grids, district_data=True)

    # Set method options
    # You can specify if the DHN is based on CO2. If not, a water DHN is assumed.
    method = {'building-scale': True, 'DHN_CO2': True}

    # Set specific parameters
    # specify the temperature of the DHN
    parameters = {'T_DHN_supply_cst': np.repeat(20.0, 4), "T_DHN_return_cst": np.repeat(15.0, 4)}

    # Run optimization
    reho = REHO(qbuildings_data=qbuildings_data, units=units, grids=grids, parameters=parameters, cluster=cluster, scenario=scenario, method=method, solver="gurobi")
    reho.get_DHN_costs()  # run one optimization forcing DHN to find costs DHN connection per house
    reho.single_optimization()  # run optimization with DHN costs

    # Save results
    reho.save_results(format=['xlsx', 'pickle'], filename='3e')
