import pandas as pd
from .types import ErrorDefinition

def validate_103():
    error = ErrorDefinition(
        code='103',
        description='The ethnicity code is either not valid or has not been entered.',
        affected_fields=['ETHNIC'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        
        header = dfs['Header']
        code_list = [
          'WBRI', 
          'WIRI', 
          'WOTH', 
          'WIRT', 
          'WROM', 
          'MWBC', 
          'MWBA', 
          'MWAS', 
          'MOTH', 
          'AIND', 
          'APKN', 
          'ABAN', 
          'AOTH', 
          'BCRB', 
          'BAFR', 
          'BOTH', 
          'CHNE', 
          'OOTH', 
          'REFU', 
          'NOBT'
        ]

        mask = header['ETHNIC'].isin(code_list)

        validation_error_mask = ~mask
        validation_error_locations = header.index[validation_error_mask]

        return {'Header': validation_error_locations.tolist()}

    return error, _validate

def validate_101():
    error = ErrorDefinition(
        code='101',
        description='Gender code is not valid.',
        affected_fields=['SEX'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        
        header = dfs['Header']
        code_list = [1, 2]

        mask = header['SEX'].isin(code_list)

        validation_error_mask = ~mask
        validation_error_locations = header.index[validation_error_mask]

        return {'Header': validation_error_locations.tolist()}

    return error, _validate

def fake_error():
    error = ErrorDefinition(
        code='1003',
        description='A fake error that fires if the child was born prior to 2006',
        affected_fields=['DOB'],
    )

    def _validate(dfs):
        if 'Header' not in dfs:
            return {}
        else:
            header = dfs['Header']
            mask = pd.to_datetime(header['DOB'], format='%d/%m/%Y', errors='coerce').dt.year <= 2006
            return {'Header': header.index[mask].tolist()}
    
    return error, _validate

def fake_error2():
    error = ErrorDefinition(
        code='2020',
        description='A fake error that fires if the child has a postcode containing F.',
        affected_fields=['HOME_POST'],
    )

    def _validate(dfs):
        if 'Episodes' not in dfs:
            return {}
        else:
            episodes = dfs['Episodes']
            mask = episodes['HOME_POST'].str.contains('F')
            return {'Episodes': episodes.index[mask].tolist()}

    return error, _validate