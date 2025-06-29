import pandas as pd
import unicodedata
import seaborn as sns
import matplotlib.pyplot as plt


weighted_columns = [
    "%", "Rate", "Ratio", "90s", "Shots", "SoT", "ShoDist", "ShoFK", "ShoPK", "PKatt",
    "PasTotCmp", "PasTotAtt", "PasTotDist", "PasTotPrgDist",
    "PasShoCmp", "PasMedCmp", "PasLonCmp",
    "PasShoAtt", "PasMedAtt", "PasLonAtt",
    "Assists", "PasAss", "Pas3rd", "PPA", "CrsPa", "PasProg", "TB", "Sw", "PasCrs",
    "SCA", "ScaPassLive", "ScaPassDead", "ScaDrib", "ScaSh", "ScaFld", "ScaDef",
    "GCA", "GcaPassLive", "GcaPassDead", "GcaDrib", "GcaSh", "GcaFld", "GcaDef",
    "Tkl", "TklWon", "TklDef3rd", "TklMid3rd", "TklAtt3rd",
    "TklDri", "TklDriAtt", "TklDriPast",
    "Blocks", "BlkSh", "Int", "Tkl+Int", "Clr",
    "Touches", "ToAtt", "ToSuc", "ToTkl",
    "Carries", "CarTotDist", "CarPrgDist", "CarProg", "Car3rd", "CPA", "CarMis", "CarDis",
    "Rec", "RecProg", "CrdY", "Fls", "Fld", "Off", "Recov", "AerWon", "AerLost"
]
colonnes_a_garder = [
    "MP", "Starts", "Min", "90s","Player","Nation","Pos","Squad","Age","Comp",
    "Goals", "Shots", "SoT", "ShoDist", "ShoFK", "ShoPK", "PKatt",
    "PasTotCmp", "PasTotAtt", "PasTotDist", "PasTotPrgDist",
    "PasShoCmp", "PasMedCmp", "PasLonCmp",
    "PasShoAtt", "PasMedAtt", "PasLonAtt",
    "Assists", "PasAss", "Pas3rd", "PPA", "CrsPA", "PasProg", "TB", "Sw", "PasCrs",
    "SCA", "ScaPassLive", "ScaPassDead", "ScaDrib", "ScaSh", "ScaFld", "ScaDef",
    "GCA", "GcaPassLive", "GcaPassDead", "GcaDrib", "GcaSh", "GcaFld", "GcaDef",
    "Tkl", "TklWon", "TklDef3rd", "TklMid3rd", "TklAtt3rd",
    "TklDri", "TklDriAtt", "TklDriPast", "Blocks", "BlkSh", "Int", "Tkl+Int", "Clr",
    "Touches", "ToAtt", "ToSuc", "ToTkl",
    "Carries", "CarTotDist", "CarPrgDist", "CarProg", "Car3rd", "CPA", "CarMis", "CarDis",
    "Rec", "RecProg",
    "CrdY", "Fls", "Fld", "Off", "Recov", "AerWon", "AerLost"
]

df = pd.read_csv('player_stats_2022_2023.csv', sep=';', encoding='latin1')
df = df[~df['Pos'].str.contains('GK')]
df = df[colonnes_a_garder]


def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(text))
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()

df['Player'] = df['Player'].apply(normalize_text)
df['Nation'] = df['Nation'].apply(normalize_text)

df['PlayerID'] = df['Player'] + '_' + df['Nation'] + '_'+df['Age'].astype(str)

def assign_unique_player_id(row):
    if row['Player'] == 'vitinha':
        if 'paris' in row['Squad'].lower() or 'psg' in row['Squad'].lower():
            return 'vitinha_psg'
        elif 'marseille' in row['Squad'].lower() or 'om' in row['Squad'].lower():
            return 'vitinha_marseille'
        else:
            return 'vitinha_' + row['Squad'].lower().replace(' ', '_')
    else:
        return row['PlayerID']


df['PlayerID'] = df.apply(assign_unique_player_id, axis=1)

def player_unify_all(df):
    all_player_ids = df['PlayerID'].unique()
    columns = df.columns

    df_result = pd.DataFrame(columns=columns)
    player_switchclub = []

    for player_id in all_player_ids:
        player_data = df[df['PlayerID'] == player_id]

        if len(player_data) > 1:
            player_switchclub.append(player_id)

            aggregated_data = {}
            for col in columns:
                if col == 'Squad':
                    squads = player_data['Squad'].unique()
                    aggregated_data[col] = '/'.join(squads)
                elif col in ['Player', 'Nation', 'Pos', 'Comp', 'PlayerID', 'Age', 'Born']:
                    aggregated_data[col] = player_data[col].iloc[0]
                elif player_data[col].dtype in ['float64', 'int64']:
                    if '%' in col or 'Rate' in col or 'Ratio' in col or col in weighted_columns :
                        weighted_sum = (player_data['Min'] * player_data[col]).sum()
                        total_minutes = player_data['Min'].sum()
                        aggregated_data[col] = round(weighted_sum / total_minutes, 2)
                    else:
                        aggregated_data[col] = player_data[col].sum()
                else:
                    aggregated_data[col] = player_data[col].iloc[0]
            df_result = pd.concat([df_result, pd.DataFrame([aggregated_data])], ignore_index=True)
        else:
            df_result = pd.concat([df_result, player_data], ignore_index=True)

    return df_result, player_switchclub


df, player_switchclub = player_unify_all(df)
df = df[df['Min'] >= 500]

df = df[df['Player'] != 'ronaldo vieira']


df.drop(columns=[
    'CrdY', 'PasTotDist', 'Nation', 'Squad', 'PlayerID', 
    'SoT', 'ShoDist', 'ShoFK', 'MP', 'Starts', '90s', 
    'PasMedCmp', 'PasLonCmp', 'PasShoCmp', 'ShoPK', 'PasTotAtt', 
    'PKatt', 'Sw', 'Age', 
    'PasShoAtt', 'PasMedAtt', 'PasLonAtt', 'PasAss', 'Pas3rd', 'TB', 'PasCrs',
    'ScaPassLive', 'ScaPassDead', 'ScaDrib', 'ScaSh', 'ScaFld', 'ScaDef',
    'GcaPassLive', 'GcaPassDead', 'GcaDrib', 'GcaSh', 'GcaFld', 'GcaDef',
    'TklDef3rd', 'TklMid3rd', 'TklAtt3rd', 'TklDriAtt', 'TklDriPast',
    'CarProg', 'Car3rd', 'RecProg', 'CarDis', 'Carries', 'CarTotDist', 
    'Off', 'Recov', 'Min', 'PasProg', 'CPA', 'BlkSh', 'ToTkl', 'CarMis', 'AerWon', 'AerLost',
    'Fld', 'Rec', 'Blocks', 'TklDri', 'Int', 'GCA','ToSuc','PPA','Clr',
    'Goals',          
    'PasTotCmp',      
    'Touches',       
    'CrsPA',          
    'Tkl',          
    'TklWon',         
    'CarPrgDist',    
    'Fls'          
], inplace=True)


df.to_csv('player_stats_processed.csv', sep=';', encoding='utf-8', index=False)
