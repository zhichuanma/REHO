from reho.model.reho import *

import pandas as pd

if __name__ == '__main__':

    INDICATORS = [
        "CCEQL", "CCEQS", "CCHHL", "CCHHS", "MAL", "MAS", "PCOX", "FWEXS", "HTXCS", "HTXNCS", "FWEXL",
        "HTXCL", "HTXNCL", "MEU", "OLD", "FWA", "PMF", "TRA", "FWEU", "IREQ", "IRHH", "LOBDV", "LTBDV",
        "TPW", "WAVFWES", "WAVHH", "WAVTES", "TTHH", "TTEQ"
    ]

    # Set building parameters
    reader = QBuildingsReader()
    qbuildings_data = reader.read_csv(buildings_filename='buildings.csv', nb_buildings=2)

    # Select clustering options for weather data
    cluster = {'Location': 'Geneva', 'Attributes': ['T', 'I', 'W'], 'Periods': 10, 'PeriodDuration': 24}

    # DataFrame to store X_min and X_max for each indicator
    df_results = pd.DataFrame(index=INDICATORS, columns=INDICATORS)

    for opt_indicator in INDICATORS:
        # Set scenario
        scenario = {
                'Objective': opt_indicator,
                'name': 'normalization',
                'exclude_units': [],
                'enforce_units': []
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
        # Store results in the DataFrame
            df_results.loc[opt_indicator, indicator] = reho.results['normalization'][0]['df_lca_Performance'].loc['Network', indicator]

    # Print the results DataFrame
    print(df_results)

    # Save the results to a CSV file
    df_results.to_csv('results_normalized.csv')

