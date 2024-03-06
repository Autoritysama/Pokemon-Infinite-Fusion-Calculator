import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Text, Label, Entry, Button, StringVar, IntVar
import math
import threading
import pickle
import os
from tkinter import ttk
import gdown

# Create the data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Download the file from Google Drive
url = 'https://drive.google.com/uc?id=1QF-Y3Mrqb2f2FxCLeYhY8cRrVRXx77Rz'
output = 'data/pokemon_fusions.xlsx'
gdown.download(url, output, quiet=False)

# Initialize the variables
fusions_df = None
pokemon_data = None

# Function to load the Excel files in the background
def load_data_background():
    global fusions_df, pokemon_data
    fusions_df = pd.read_excel('data/pokemon_fusions.xlsx')
    pokemon_data = pd.read_csv('data/pokemon.csv')
    # Cache the data after loading
    cache_data()

# Function to cache the loaded data
def cache_data():
    if fusions_df is not None and pokemon_data is not None:
        with open('data_cache.pkl', 'wb') as f:
            pickle.dump((fusions_df, pokemon_data), f)

# Function to load the cached data
def load_cached_data():
    global fusions_df, pokemon_data
    try:
        with open('data_cache.pkl', 'rb') as f:
            fusions_df, pokemon_data = pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        print("Cache file is empty or corrupted. Loading data from Excel files.")
        load_data_background()

# Check if the cache file exists
if os.path.exists('data_cache.pkl'):
    # Load the cached data
    load_cached_data()
else:
    # Start a background thread to load the Excel files
    threading.Thread(target=load_data_background).start()

# Rest of your code....

def show_results(results):
    result_window = Toplevel(root)
    result_window.title("Fusion Results")

    # Create a new Treeview widget each time
    tree = ttk.Treeview(result_window)
    tree.pack(fill="both", expand=True)

    # Define the columns
    columns = ['Head', 'Body', 'Type 1', 'Type 2', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total Stats']
    tree["columns"] = columns

    # Format column headers
    for col in columns:
        tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(tree, _col, False))
        tree.column(col, width=100, anchor="center")

    # Round the stats to the inferior unit and convert to integer
    results_rounded = results.copy()
    stats_columns = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total Stats']
    results_rounded[stats_columns] = results_rounded[stats_columns].apply(lambda x: x.astype(float).apply(math.floor).astype(int))

    # Replace NaN values in 'Type 2' with an empty string
    results_rounded['Type 2'] = results_rounded['Type 2'].fillna('')

    # Reorder the columns
    results_rounded = results_rounded[columns]

    # Add data to the Treeview
    for _, row in results_rounded.iterrows():
        tree.insert("", "end", values=list(row))

def treeview_sort_column(tv, col, reverse):
    # Get the data to be sorted
    data = [(tv.set(k, col), k) for k in tv.get_children("")]

    # Determine the data type of the column
    if col in ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total Stats']:
        # Sort numeric columns as integers
        data.sort(key=lambda x: int(x[0]), reverse=reverse)
    else:
        # Sort other columns as strings
        data.sort(reverse=reverse)

    # Rearrange items in sorted positions
    for index, (_, k) in enumerate(data):
        tv.move(k, "", index)

    # Reverse sort next time
    tv.heading(col, command=lambda _col=col: treeview_sort_column(tv, _col, not reverse))


def find_closest_fusions(target_stats, weights, num_results, locked=None, locked_head=None, locked_body=None, type1=None, type2=None, exclude_legendary=False, exclude_mega=False, excluded_pokemon=None):
    # Filter fusions if a Pokémon is locked
    if locked:
        fusions = fusions_df[(fusions_df['Head'] == locked) | (fusions_df['Body'] == locked)]
    elif locked_head:
        fusions = fusions_df[fusions_df['Head'] == locked_head]
    elif locked_body:
        fusions = fusions_df[fusions_df['Body'] == locked_body]
    else:
        fusions = fusions_df.copy()  # Create a copy of fusions_df

    if excluded_pokemon:
        excluded_pokemon = [pokemon.strip() for pokemon in excluded_pokemon]  # Remove leading/trailing whitespace
        fusions = fusions[~((fusions['Head'].isin(excluded_pokemon)) & (fusions['Body'].isin(excluded_pokemon)))]

    # Filter out Legendary Pokémon if requested
    if exclude_legendary:
        legendary_pokemon = pokemon_data[pokemon_data['Legendary'] == True]['Name']
        fusions = fusions[~fusions['Head'].isin(legendary_pokemon) & ~fusions['Body'].isin(legendary_pokemon)]

    if exclude_mega:
        mega_pokemon_names = pokemon_data[pokemon_data['Name'].str.contains("Mega", case=False, na=False)]['Name'].tolist()
        fusions = fusions[~fusions['Head'].isin(mega_pokemon_names) & ~fusions['Body'].isin(mega_pokemon_names)]

    # Get the type info from pokemon_data
    type_info = pokemon_data.set_index('Name')[['Type 1', 'Type 2']]

    # If type filtering is requested
    if type1 or type2:
        # Filter fusions based on type conditions using vectorized operations
        head_type1 = type_info.loc[fusions['Head'], 'Type 1'].values
        head_type2 = type_info.loc[fusions['Head'], 'Type 2'].values
        body_type1 = type_info.loc[fusions['Body'], 'Type 1'].values
        body_type2 = type_info.loc[fusions['Body'], 'Type 2'].values

        # Calculate the fusion types based on the head and body types
        fusion_primary_type = head_type1
        fusion_secondary_type = body_type2.copy()
        fusion_secondary_type[pd.isnull(fusion_secondary_type)] = body_type1[pd.isnull(fusion_secondary_type)]
        fusion_secondary_type[fusion_primary_type == fusion_secondary_type] = None

        # Check if the fusion types match the desired types
        if not type2:
            type_mask = (fusion_primary_type == type1) & pd.isnull(fusion_secondary_type)
        else:
            type_mask = (fusion_primary_type == type1) & (fusion_secondary_type == type2)

        fusions = fusions[type_mask]

    if fusions.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no matches are found
    
    # Calculate scores based on absolute difference from target stats, applying weights
    scores = pd.Series(0, index=fusions.index)
    for stat, target in target_stats.items():
        if target > 0:
            scores += weights[stat] * (fusions[stat] - target).abs()

    # Get the indices of the closest matches
    closest_indices = scores.nsmallest(num_results).index

    # Calculate the total stats for each fusion
    fusions.loc[closest_indices, 'Total Stats'] = fusions.loc[closest_indices, ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']].sum(axis=1)

    closest_fusions = fusions.loc[closest_indices]

    # Calculate the fusion types for each fusion
    fusion_primary_type = type_info.loc[closest_fusions['Head'], 'Type 1'].values
    fusion_secondary_type = type_info.loc[closest_fusions['Body'], 'Type 2'].values
    fusion_secondary_type[pd.isnull(fusion_secondary_type)] = type_info.loc[closest_fusions['Body'], 'Type 1'].values[pd.isnull(fusion_secondary_type)]
    fusion_secondary_type[fusion_primary_type == fusion_secondary_type] = None

    # Add the calculated fusion types to the DataFrame
    closest_fusions['Type 1'] = fusion_primary_type
    closest_fusions['Type 2'] = fusion_secondary_type

    return closest_fusions

# GUI pour entrer les stats recherchées et afficher les résultats
def search_fusions():
    # Créer une nouvelle fenêtre pour entrer les stats cibles
    input_window = Toplevel(root)
    input_window.title("Enter Target Stats")
    
    labels = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']
    entries = {label: Entry(input_window, width=5) for label in labels}
    weights = {label: StringVar(input_window, value='1') for label in labels}
    
    # Créer les champs pour entrer les stats et les poids
    for i, label in enumerate(labels):
        Label(input_window, text=label).grid(row=i, column=0)
        entries[label].grid(row=i, column=1)
        Entry(input_window, textvariable=weights[label], width=5).grid(row=i, column=2)
    
    # Option pour verrouiller la tête d'un Pokémon dans la fusion
    Label(input_window, text="Lock Head:").grid(row=len(labels), column=0)
    lock_head = Entry(input_window, width=20)
    lock_head.grid(row=len(labels), column=1, columnspan=2)

    # Option pour verrouiller le corps d'un Pokémon dans la fusion
    Label(input_window, text="Lock Body:").grid(row=len(labels)+1, column=0)
    lock_body = Entry(input_window, width=20)
    lock_body.grid(row=len(labels)+1, column=1, columnspan=2)

    # Option pour définir le nombre de résultats
    Label(input_window, text="Num Results:").grid(row=len(labels)+2, column=0)
    num_results_entry = Entry(input_window, width=5)
    num_results_entry.grid(row=len(labels)+2, column=1)
    num_results_entry.insert(0, "5")  # Default value for num results

    # Option to lock a Pokémon without specifying head or body
    Label(input_window, text="Lock Any:").grid(row=len(labels)+3, column=0)
    lock_any = Entry(input_window, width=20)
    lock_any.grid(row=len(labels)+3, column=1, columnspan=2)

    # Options to specify type
    Label(input_window, text="Type 1:").grid(row=len(labels)+4, column=0)
    type1_entry = Entry(input_window, width=20)
    type1_entry.grid(row=len(labels)+4, column=1, columnspan=2)

    Label(input_window, text="Type 2:").grid(row=len(labels)+5, column=0)
    type2_entry = Entry(input_window, width=20)
    type2_entry.grid(row=len(labels)+5, column=1, columnspan=2)

    # Checkbox for excluding Legendary Pokémon
    exclude_legendary_var = IntVar()
    tk.Checkbutton(input_window, text="No Legendary", variable=exclude_legendary_var).grid(row=len(labels)+6, column=0, columnspan=3)

    # Checkbox for excluding Mega Evolutions
    exclude_mega_var = IntVar()
    tk.Checkbutton(input_window, text="Exclude Mega Evolutions", variable=exclude_mega_var).grid(row=len(labels)+7, column=0, columnspan=3)

    # Option to exclude specific Pokémon
    Label(input_window, text="Exclude Pokémon (comma-separated):").grid(row=len(labels)+8, column=0)
    exclude_pokemon_entry = Entry(input_window, width=20)
    exclude_pokemon_entry.grid(row=len(labels)+8, column=1, columnspan=2)

    # Modify the call to on_submit to pass the correct arguments
    submit_button = Button(input_window, text="Submit", command=lambda: on_submit(
        entries, weights, num_results_entry.get(), lock_head.get(), lock_body.get(),
        lock_any.get(), type1_entry.get(), type2_entry.get(),
        exclude_legendary_var.get(), exclude_mega_var.get(), exclude_pokemon_entry.get()))
    submit_button.grid(row=len(labels)+9, columnspan=3)

def on_submit(entries, weights, num_results, locked_head, locked_body, locked_any, type1, type2, exclude_legendary, exclude_mega, excluded_pokemon):
    # Récupérer les stats cibles et les poids depuis les entrées
    target_stats = {label: int(entry.get()) if entry.get() else 0 for label, entry in entries.items()}
    weights_dict = {label: float(weight.get()) for label, weight in weights.items()}
    num_results = int(num_results)
    locked_head = locked_head if locked_head else None
    locked_body = locked_body if locked_body else None
    locked = locked_any if locked_any else None
    type1 = type1 if type1 else None
    type2 = type2 if type2 else None
    # Convert exclude_legendary from IntVar to boolean
    exclude_legendary_bool = bool(exclude_legendary)
    # Convert exclude_mega from IntVar to boolean
    exclude_mega_bool = bool(exclude_mega)

    # Convert excluded_pokemon from string to list
    excluded_pokemon_list = excluded_pokemon.split(',') if excluded_pokemon else None
    
    closest_fusions = find_closest_fusions(target_stats, weights_dict, num_results, locked, locked_head, locked_body, type1, type2, exclude_legendary_bool, exclude_mega_bool, excluded_pokemon_list)

    if not closest_fusions.empty:
        show_results(closest_fusions)
    else:
        messagebox.showinfo("No Results", "No fusions found matching the criteria.")
    

# Résistances des types Pokémon
type_resistances = {
    'Normal': [],
    'Fire': ['Fire', 'Grass', 'Ice', 'Bug', 'Steel', 'Fairy'],
    'Water': ['Fire', 'Water', 'Ice', 'Steel'],
    'Electric': ['Electric', 'Flying', 'Steel'],
    'Grass': ['Water', 'Electric', 'Grass', 'Ground'],
    'Ice': ['Ice'],
    'Fighting': ['Bug', 'Rock', 'Dark'],
    'Poison': ['Grass', 'Fighting', 'Poison', 'Bug', 'Fairy'],
    'Ground': ['Poison', 'Rock'],
    'Flying': ['Grass', 'Fighting', 'Bug'],
    'Psychic': ['Fighting', 'Psychic'],
    'Bug': ['Grass', 'Fighting', 'Ground'],
    'Rock': ['Normal', 'Fire', 'Poison', 'Flying'],
    'Ghost': ['Poison', 'Bug'],
    'Dragon': ['Fire', 'Water', 'Electric', 'Grass'],
    'Dark': ['Ghost', 'Dark'],
    'Steel': ['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 'Bug', 'Rock', 'Dragon', 'Steel', 'Fairy'],
    'Fairy': ['Fighting', 'Bug', 'Dark']
}

# Faiblesses des types Pokémon
type_weaknesses = {
    'Normal': ['Fighting'],
    'Fire': ['Water', 'Ground', 'Rock'],
    'Water': ['Electric', 'Grass'],
    'Electric': ['Ground'],
    'Grass': ['Fire', 'Ice', 'Poison', 'Flying', 'Bug'],
    'Ice': ['Fire', 'Fighting', 'Rock', 'Steel'],
    'Fighting': ['Flying', 'Psychic', 'Fairy'],
    'Poison': ['Ground', 'Psychic'],
    'Ground': ['Water', 'Grass', 'Ice'],
    'Flying': ['Electric', 'Ice', 'Rock'],
    'Psychic': ['Bug', 'Ghost', 'Dark'],
    'Bug': ['Fire', 'Flying', 'Rock'],
    'Rock': ['Water', 'Grass', 'Fighting', 'Ground', 'Steel'],
    'Ghost': ['Ghost', 'Dark'],
    'Dragon': ['Ice', 'Dragon', 'Fairy'],
    'Dark': ['Fighting', 'Bug', 'Fairy'],
    'Steel': ['Fire', 'Fighting', 'Ground'],
    'Fairy': ['Poison', 'Steel']
}

# Immunités des types Pokémon
type_immunities = {
    'Normal': ['Ghost'],
    'Fire': [],
    'Water': [],
    'Electric': [],
    'Grass': [],
    'Ice': [],
    'Fighting': [],
    'Poison': [],
    'Ground': ['Electric'],
    'Flying': ['Ground'],
    'Psychic': [],
    'Bug': [],
    'Rock': [],
    'Ghost': ['Normal', 'Fighting'],
    'Dragon': [],
    'Dark': ['Psychic'],
    'Steel': ['Poison'],
    'Fairy': ['Dragon']
}

# Function to swap the input values of head and body, and recalculate stats
def swap_and_recalculate():
    # Swap the values of the entries
    head_pokemon = entry_head.get()
    body_pokemon = entry_body.get()
    entry_head.delete(0, tk.END)
    entry_head.insert(0, body_pokemon)
    entry_body.delete(0, tk.END)
    entry_body.insert(0, head_pokemon)
    # Recalculate after swapping
    on_calculate()


# Fonction pour déterminer les faiblesses, résistances et immunités du type fusionné
def calculate_type_advantages(fusion_type):
    # Obtenir les faiblesses, résistances et immunités pour chaque type
    type1_weaknesses = set(type_weaknesses[fusion_type[0]])
    type2_weaknesses = set(type_weaknesses.get(fusion_type[1], []))
    type1_resistances = set(type_resistances[fusion_type[0]])
    type2_resistances = set(type_resistances.get(fusion_type[1], []))
    type1_immunities = set(type_immunities[fusion_type[0]])
    type2_immunities = set(type_immunities.get(fusion_type[1], []))

    # Calculer les immunités combinées
    combined_immunities = type1_immunities | type2_immunities

    # Calculer les doubles faiblesses et résistances
    double_weaknesses = type1_weaknesses & type2_weaknesses
    double_resistances = type1_resistances & type2_resistances

    # Calculer les faiblesses et résistances simples
    single_weaknesses = (type1_weaknesses | type2_weaknesses) - double_weaknesses - double_resistances - combined_immunities
    single_resistances = (type1_resistances | type2_resistances) - double_resistances - single_weaknesses - combined_immunities

    # Les faiblesses et résistances se neutralisent si elles sont présentes dans les deux types
    neutral_types = (type1_weaknesses & type2_resistances) | (type1_resistances & type2_weaknesses)
    single_weaknesses -= neutral_types
    single_resistances -= neutral_types

    # Les faiblesses/résistances doubles prennent la priorité sur les simples, donc on les enlève des simples
    single_weaknesses -= double_weaknesses
    single_resistances -= double_resistances

    # Retourner les statistiques combinées
    return single_weaknesses, double_weaknesses, single_resistances, double_resistances, combined_immunities

# Fonction pour calculer les stats fusionnées
def calculate_fusion_stats(head, body, pokemon_data):
    # Get the stats for the head and body Pokémon
    head_stats = pokemon_data.loc[pokemon_data['Name'].str.lower() == head.lower()].iloc[0]
    body_stats = pokemon_data.loc[pokemon_data['Name'].str.lower() == body.lower()].iloc[0]

    # Start with the primary type of the head Pokémon
    fusion_primary_type = head_stats['Type 1']

    # If the body Pokémon has a secondary type, use that. Otherwise, use its primary type
    if pd.notnull(body_stats['Type 2']):
        fusion_secondary_type = body_stats['Type 2']
    else:
        fusion_secondary_type = body_stats['Type 1']

    # If the primary type of the head is the same as the primary or secondary type of the body, it will only have one type
    if fusion_primary_type == fusion_secondary_type:
        fusion_secondary_type = None

    # Calculate the fusion stats and round down to the inferior unit
    fusion_stats = {
        'HP': math.floor((2 * head_stats['HP'] + body_stats['HP']) / 3),
        'Attack': math.floor((2 * body_stats['Attack'] + head_stats['Attack']) / 3),
        'Defense': math.floor((2 * body_stats['Defense'] + head_stats['Defense']) / 3),
        'Sp. Atk': math.floor((2 * head_stats['Sp. Atk'] + body_stats['Sp. Atk']) / 3),
        'Sp. Def': math.floor((2 * head_stats['Sp. Def'] + body_stats['Sp. Def']) / 3),
        'Speed': math.floor((2 * body_stats['Speed'] + head_stats['Speed']) / 3),
        'Type 1': fusion_primary_type,
        'Type 2': fusion_secondary_type
    }

    return fusion_stats

def on_calculate():
    head_pokemon = entry_head.get()
    body_pokemon = entry_body.get()
    
    if not head_pokemon or not body_pokemon:
        messagebox.showerror("Error", "Please enter both Pokémon names.")
        return

    try:
        fusion_stats = calculate_fusion_stats(head_pokemon, body_pokemon, pokemon_data)
        single_weaknesses, double_weaknesses, single_resistances, double_resistances, combined_immunities = calculate_type_advantages((fusion_stats['Type 1'], fusion_stats['Type 2']))
        
        # Formatage des résultats pour l'affichage
        weaknesses = ' '.join([f"{w} x2" for w in single_weaknesses] + [f"{w} x4" for w in double_weaknesses])
        resistances = ' '.join([f"{r} x0.5" for r in single_resistances] + [f"{r} x0.25" for r in double_resistances])
        immunities = ' '.join([f"{i} immune" for i in combined_immunities])

        result_stats.set(f"HP: {fusion_stats['HP']}\n"
                         f"Attack: {fusion_stats['Attack']}\n"
                         f"Defense: {fusion_stats['Defense']}\n"
                         f"Sp. Atk: {fusion_stats['Sp. Atk']}\n"
                         f"Sp. Def: {fusion_stats['Sp. Def']}\n"
                         f"Speed: {fusion_stats['Speed']}")

        # Mise à jour de l'affichage des types
        type_display = f"{fusion_stats['Type 1']}"
        if fusion_stats['Type 2']:
            type_display += f" / {fusion_stats['Type 2']}"

        result_type.set(f"Type: {type_display}\n"
                        f"Weaknesses: {weaknesses}\n"
                        f"Resistances: {resistances}\n"
                        f"Immunities: {immunities}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")



# Création de la fenêtre principale
root = tk.Tk()
root.title("Pokémon Fusion Calculator")

# Ajout d'étiquettes pour les champs de saisie
label_head = tk.Label(root, text="Head Pokémon")
label_head.pack()
entry_head = tk.Entry(root, width=30)
entry_head.pack()

label_body = tk.Label(root, text="Body Pokémon")
label_body.pack()
entry_body = tk.Entry(root, width=30)
entry_body.pack()

# Création du bouton de calcul
button_calculate = tk.Button(root, text="Calculate", command=on_calculate)
button_calculate.pack()

search_button = tk.Button(root, text="Search Fusions", command=search_fusions)
search_button.pack()

# Création des zones de texte pour les résultats
result_stats = tk.StringVar()
label_result_stats = tk.Label(root, textvariable=result_stats, justify=tk.LEFT)
label_result_stats.pack()

result_type = tk.StringVar()
label_result_type = tk.Label(root, textvariable=result_type, justify=tk.LEFT)
label_result_type.pack()

# Creating a button for swapping head and body input values
swap_button = tk.Button(root, text="Swap & Recalculate", command=swap_and_recalculate)
swap_button.pack()


# Lancement de la boucle principale de tkinter
root.mainloop()
