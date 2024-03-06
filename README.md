# Pokemon Infinite Fusion Calculator

This Python script allows you to calculate the stats and type advantages of fused Pokémon and search for the closest matching fusions based on target stats and various filtering options.

## Features

- Calculate the stats (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed) of a fused Pokémon based on the head and body Pokémon.
- Determine the type, weaknesses, resistances, and immunities of the fused Pokémon.
- Search for the closest matching fusions based on target stats and filtering criteria.
- User-friendly tkinter interface for inputting Pokémon and displaying results.
- Utilizes pandas for data manipulation and analysis.
- Sort the search results by clicking on the stats column headers in ascending or descending order.
- Assign weights to each stat to prioritize their importance in the search process.
- Specify 0 for stats you don't care about and keep the weight at 1 for those stats.

![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/12092193-992e-4f83-991f-45d25a737663)
![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/be6b4588-55c9-4dac-8ea4-47399b066158)
![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/30fec83f-140e-4656-a31b-e68ae8611ddc)


![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/5c2e27e1-9280-47a9-90cf-7452db760079)

If you get this error try to swap the Type 1 and Type 2 or remove verify that the typing is correctly written (WITH A UPPERCASE A THE BEGINNING)

## Requirements

- Python 3.x
- pandas
- tkinter

## Setup

1. Clone the repository and navigate to the project directory.
2. Install the required dependencies using `pip install -r requirements.txt`.

## Usage

### Calculating Fused Pokémon Stats

1. Run the script using `python pokemon_fusion.py`.
2. In the main window, enter the names of the head and body Pokémon in the respective entry fields.
3. Click the "Calculate" button to calculate the stats and type advantages of the fused Pokémon.
4. The resulting stats (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed) and type information (type, weaknesses, resistances, immunities) will be displayed in the labeled areas below the button.

### Searching for Closest Matching Fusions

1. In the main window, click the "Search Fusions" button to open the search interface.
2. In the search window, enter the target stats for each stat (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed) in the respective entry fields.
   - You can also specify weights for each stat in the adjacent entry fields.
   - The weights determine the importance of each stat in the search process.
   - Weights can range from 1 to 10, with 10 being the most important and 1 being the least important.
   - By default, all weights are set to 1, giving equal importance to all stats.
   - Increasing the weight of a stat will prioritize fusions that closely match the target value for that stat.
   - If you don't care about a specific stat, you can set its target value to 0 and keep the weight at 1.
3. Optionally, you can specify the following filtering criteria:
   - Lock Head: Enter the name of a Pokémon to lock as the head of the fusion.
   - Lock Body: Enter the name of a Pokémon to lock as the body of the fusion.
   - Lock Any: Enter the name of a Pokémon to lock in either the head or body position.
   - Type 1: Enter the desired primary type of the fused Pokémon.
   - Type 2: Enter the desired secondary type of the fused Pokémon.
   - Exclude Legendary: Check the box to exclude legendary Pokémon from the search results.
   - Exclude Mega Evolutions: Check the box to exclude mega evolutions from the search results.
   - Exclude Pokémon: Enter a comma-separated list of Pokémon names to exclude from the search results.
4. Specify the number of desired results in the "Num Results" entry field.
5. Click the "Submit" button to initiate the search.
6. The search results will be displayed in a new window, showing the closest matching fusions based on the target stats, weights, and filtering criteria.
   - The results include the head and body Pokémon, types, stats, and total stats of each fusion.
   - The results are sorted based on the closeness to the target stats, considering the assigned weights.
   - You can click on the column headers to sort the results based on that column in ascending or descending order.

### Additional Features

- Swapping Head and Body: In the main window, you can click the "Swap & Recalculate" button to swap the head and body Pokémon and automatically recalculate the stats and type advantages of the swapped fusion.

Feel free to explore and experiment with different combinations of head and body Pokémon, target stats, weights, and filtering options to discover interesting and powerful fusions!

Note: The script relies on the data from the `pokemon_fusions.xlsx` and `pokemon.csv` files, which should be placed in the `data` directory relative to the script.
