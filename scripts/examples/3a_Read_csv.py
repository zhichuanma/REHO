from reho.model.reho import *


if __name__ == '__main__':

    buildings_filename = str(Path(__file__).parent / 'data' / 'buildings.csv')

    # Set building parameters
    # Load your buildings from a csv file instead of reading the database
    reader = QBuildingsReader()
    qbuildings_data = reader.read_csv(buildings_filename=buildings_filename, nb_buildings=40)

    # Select clustering options for weather data
    cluster = {'Location': 'Sion', 'Attributes': ['T', 'I', 'W'], 'Periods': 10, 'PeriodDuration': 24}

    # Set scenario
    scenario = dict()
    scenario['Objective'] = 'LOBDV'
    scenario['name'] = 'totex'
    scenario['exclude_units'] = []
    scenario['enforce_units'] = []

    # Initialize available units and grids
    grids = infrastructure.initialize_grids()
    units = infrastructure.initialize_units(scenario, grids)

    # Set method options
    method = {'building-scale': True, 'save_lca': True}

    # Run optimization
    reho = REHO(qbuildings_data=qbuildings_data, units=units, grids=grids, cluster=cluster, scenario=scenario, method=method, solver="gurobi")
    reho.single_optimization()

    # Save results
    reho.save_results(format=['xlsx', 'pickle'], filename='2a')

    from reho.plotting import plotting
    import pandas as pd

    results = pd.read_pickle(r'C:\Users\Administrator\PycharmProjects\REHO\scripts\examples\results\2a.pickle')
    plotting.plot_performance(results, plot='gwp', indexed_on='Scn_ID', filename="figures/performance_gwp").show()
    plotting.plot_performance(results, plot='combined', indexed_on='Scn_ID', filename="figures/performance_combined").show()
    plotting.plot_sankey(results['totex'][0], label='EN_long', color='ColorPastel').show()
    plotting.plot_sunburst_eud(results, label='EN_long').show()
    units_to_plot = ['ElectricalHeater', 'HeatPump', 'PV', 'NG_Boiler']
    plotting.plot_profiles(results['totex'][0], units_to_plot, label='EN_long', color='ColorPastel',
                           resolution='weekly').show()