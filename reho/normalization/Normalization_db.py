from reho.model.reho import *

import pandas as pd

if __name__ == '__main__':

    df_building_units = pd.read_csv(
        r'C:\Users\Administrator\PycharmProjects\REHO\reho\data\infrastructure\building_units.csv')
    df_district_units = pd.read_csv(
        r'C:\Users\Administrator\PycharmProjects\REHO\reho\data\infrastructure\district_units.csv')
    df_grids = pd.read_csv(
        r'C:\Users\Administrator\PycharmProjects\REHO\reho\data\infrastructure\grids.csv')

    INDICATORS = [
        "CCEQL", "CCEQS", "CCHHL", "CCHHS", "MAL", "MAS", "PCOX", "FWEXS", "HTXCS", "HTXNCS", "FWEXL",
        "HTXCL", "HTXNCL", "MEU", "OLD", "FWA", "PMF", "TRA", "FWEU", "IREQ", "IRHH", "LOBDV", "LTBDV",
        "TPW", "WAVFWES", "WAVHH", "WAVTES", "TTHH", "TTEQ"
    ]

    # Building Units
    BU = df_building_units['Unit']

    # District Units
    DU = df_district_units['Unit']

    # Grid
    GU = df_grids['Grid']

    # Set building parameters
    reader = QBuildingsReader()
    qbuildings_data = reader.read_csv(buildings_filename='buildings.csv', nb_buildings=1)

    # Select clustering options for weather data
    cluster = {'Location': 'Geneva', 'Attributes': ['T', 'I', 'W'], 'Periods': 10, 'PeriodDuration': 24}

    df_results = pd.DataFrame(index=INDICATORS, columns=INDICATORS)
    df_X_max_X_min = pd.DataFrame(index=['X_min', 'X_max'], columns=INDICATORS)

    for unit in BU:
        for opt_indicator in INDICATORS:
            scenario = {
                'Objective': opt_indicator,
                'name': 'normalization_db',
                'exclude_units': [],
                'enforce_units': [unit]
                }

            # Initialize available units and grids
            grids = infrastructure.initialize_grids()
            units = infrastructure.initialize_units(scenario, grids)

            # Set method options
            method = {'building-scale': True, 'save_lca': True}

            # Run optimization
            reho = REHO(
                qbuildings_data=qbuildings_data,
                units=units,
                grids=grids,
                cluster=cluster,
                scenario=scenario,
                method=method,
                solver="gurobi"
                )
            reho.single_optimization()

            for indicator in INDICATORS:
                df_results.loc[opt_indicator, indicator] = reho.results['normalization_db'][0]['df_lca_Units'].loc[ unit + '_Building1', indicator]/reho.results['normalization_db'][0]['df_Unit'].loc[ unit + '_Building1', 'Units_Mult']

        df_X_max_X_min.loc['X_max'] = df_results.max()
        df_X_max_X_min.loc['X_min'] = df_results.min()

        df_results.to_csv('results_normalized.csv')
        df_X_max_X_min.to_csv('X_max_X_min.csv')

        Normalization_db = {
            unit: {
                'df_results': df_results,
                'df_X_max_X_min': df_X_max_X_min
            }
        }

    # To be continued
