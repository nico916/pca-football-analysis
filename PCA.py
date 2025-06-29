import pandas as pd
import unicodedata
import seaborn as sns
import matplotlib.pyplot as plt

# Liste des colonnes à calculer de manière pondérée
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
    # Temps de jeu
    "MP", "Starts", "Min", "90s","Player","Nation","Pos","Squad","Age","Comp",
    
    # Statistiques Offensives
    "Goals", "Shots", "SoT", "ShoDist", "ShoFK", "ShoPK", "PKatt",
    
    # Statistiques de Passes
    "PasTotCmp", "PasTotAtt", "PasTotDist", "PasTotPrgDist",
    "PasShoCmp", "PasMedCmp", "PasLonCmp",
    "PasShoAtt", "PasMedAtt", "PasLonAtt",
    "Assists", "PasAss", "Pas3rd", "PPA", "CrsPA", "PasProg", "TB", "Sw", "PasCrs",
    
    # Actions Créant des Tirs et des Buts
    "SCA", "ScaPassLive", "ScaPassDead", "ScaDrib", "ScaSh", "ScaFld", "ScaDef",
    "GCA", "GcaPassLive", "GcaPassDead", "GcaDrib", "GcaSh", "GcaFld", "GcaDef",
    
    # Statistiques Défensives
    "Tkl", "TklWon", "TklDef3rd", "TklMid3rd", "TklAtt3rd",
    "TklDri", "TklDriAtt", "TklDriPast", "Blocks", "BlkSh", "Int", "Tkl+Int", "Clr",
    
    # Possession et Dribbles
    "Touches", "ToAtt", "ToSuc", "ToTkl",
    "Carries", "CarTotDist", "CarPrgDist", "CarProg", "Car3rd", "CPA", "CarMis", "CarDis",
    "Rec", "RecProg",
    
    # Discipline et Autres
    "CrdY", "Fls", "Fld", "Off", "Recov", "AerWon", "AerLost"
]



# Charger les données

df = pd.read_csv('player_stats_2022_2023.csv', sep=';', encoding='latin1')
df = df[~df['Pos'].str.contains('GK')]
df = df[colonnes_a_garder]
# Supprimer les gardiens


# Fonction pour normaliser les chaînes de caractères
def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(text))
        if unicodedata.category(c) != 'Mn'
    ).lower().strip()

# Appliquer la normalisation aux noms des joueurs et des nations
df['Player'] = df['Player'].apply(normalize_text)
df['Nation'] = df['Nation'].apply(normalize_text)

# Créer un identifiant unique pour chaque joueur
df['PlayerID'] = df['Player'] + '_' + df['Nation'] + '_'+df['Age'].astype(str)

# Fonction pour attribuer un PlayerID unique aux deux Vitinha
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

# Appliquer la fonction au DataFrame
df['PlayerID'] = df.apply(assign_unique_player_id, axis=1)
# Agrégation des joueurs avant filtrage sur les minutes jouées
def player_unify_all(df):
    all_player_ids = df['PlayerID'].unique()
    columns = df.columns

    df_result = pd.DataFrame(columns=columns)
    player_switchclub = []

    for player_id in all_player_ids:
        player_data = df[df['PlayerID'] == player_id]

        if len(player_data) > 1:
            # Le joueur a changé de club
            player_switchclub.append(player_id)

            # Agréger les données
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

# Appliquer l'agrégation
df, player_switchclub = player_unify_all(df)

# Filtrer les joueurs ayant joué moins de 500 minutes
df = df[df['Min'] >= 500]

df = df[df['Player'] != 'ronaldo vieira']  # Enlever le joueur Ronaldo Vieira
#df = df[df['Comp'] == 'Ligue 1'] 

df.drop(columns=[
    # Déjà supprimées
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
    
    # Nouvelles suppressions
    'Goals',          # Très lié à Goals
    'PasTotCmp',      # Trop général par rapport à PasTotPrgDist
    'Touches',        # Trop général par rapport à ToAtt
    'CrsPA',          # Incluse dans SCA
    'Tkl',            # Déjà représentée par Tkl+Int
    'TklWon',         # Déjà représentée par Tkl+Int
    'CarPrgDist',     # Liée à ToAtt ou SCA
    'Fls'             # Moins significative
], inplace=True)


# Enregistrer le DataFrame final
df.to_csv('player_stats_processed.csv', sep=';', encoding='utf-8', index=False)