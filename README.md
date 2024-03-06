# Pokemon Infinite Fusion Calculator

![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/08b8897a-84a1-466f-ad8c-4bd383268588)

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

  
## Fusion Stat Calculator - Main Menu
![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/12092193-992e-4f83-991f-45d25a737663)

Look at the excel file pokemon.csv to find all the Pokemon available and their names. Sometime spelling can be different for Pokemon like Aegislash and some others.

To calculate the stats and type information for a fused Pokémon, follow these steps:

1. Enter the names of the Head Pokémon and Body Pokémon in their respective fields.
   - Make sure the names are spelled correctly and match the capitalization used in the Pokémon games.

2. Click the "Calculate" button to generate the results.

3. The calculated stats for the fused Pokémon will be displayed, including:
   - HP, Attack, Defense, Sp. Atk, Sp. Def, and Speed

4. The type information for the fusion will also be shown, including:
   - Primary Type (Type 1) and Secondary Type (Type 2)
   - Weaknesses (2x and 4x)
   - Resistances (0.5x and 0.25x)
   - Immunities

5. If you want to quickly swap the Head and Body Pokémon and recalculate the results, click the "Swap & Recalculate" button.

For more advanced searching capabilities, click the "Search Fusions" button to access the Fusion Search Criteria interface.

## Fusion Search Criteria 
![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/be6b4588-55c9-4dac-8ea4-47399b066158)

When entering your search criteria, please ensure that the names of Pokémon and types are spelled correctly with proper capitalization (e.g., "Garchomp", "Dragon").

- Target Stats:
  - Enter the desired values for each stat (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed).
  - Use 0 for stats you don't have a preference for.
  - Adjust the weights (1-10) to prioritize the importance of each stat in the search.

- Lock Head/Body/Any:
  - Specify a Pokémon name to lock in the head, body, or either position of the fusion.

- Num Results:
  - Choose the number of fusion results to display.

- Type 1/2:
  - Enter the desired primary and secondary types for the fusion.

- No Legendary:
  - Check this box to exclude legendary Pokémon from the results.

- Exclude Mega Evolutions:
  - Check this box to exclude Mega Evolutions from the results.

- Exclude Pokémon:
  - Enter the names of any Pokémon to exclude, separated by commas.

After filling in your search criteria, click "Submit" to view the closest matching fusions. The results will be sorted based on the specified target stats and weights. Click on the column headers to sort the results as needed.

## Fusion Search Results
![image](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/30fec83f-140e-4656-a31b-e68ae8611ddc)

After performing a search using the Fusion Search Criteria, the results will be displayed in the Fusion Results window. This screen presents the closest matching fusions based on your specified criteria.

- The results are shown in a table format, with each row representing a unique fusion.
- The columns display various information about each fusion, including:
  - Head: The Pokémon used as the head of the fusion
  - Body: The Pokémon used as the body of the fusion
  - Type 1 and Type 2: The primary and secondary types of the fusion
  - HP, Attack, Defense, Sp. Atk, Sp. Def, Speed: The individual stats of the fusion
  - Total Stats: The sum of all the individual stats

- By default, the results are sorted based on the closeness to the target stats and weights you specified in the search criteria.
- However, you can easily sort the results based on any of the columns by clicking on the respective column header.
  - Clicking once will sort the column in ascending order.
  - Clicking again will sort the column in descending order.
  - This allows you to quickly analyze and compare the fusions based on specific stats or attributes.

## Errors
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

## Support the Project

![310356803-6003bbe7-0dd3-4ca9-8e4d-b78d781f42f2 (1)](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/e6a56d4a-9f66-4e59-b483-7035ac6983a7)

If you find this Pokémon Fusion Calculator helpful and would like to support its development, you can buy me a coffee! Your contribution will be greatly appreciated and will help me continue improving the project

![Designer (6) (1)](https://github.com/Autoritysama/Pokemon-Infinite-Fusion-Calculator/assets/121148901/e378df7c-99ca-49ce-840d-e0dc0c66248f)
https://www.buymeacoffee.com/autoritysama
