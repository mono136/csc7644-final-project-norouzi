"""
Main entry point for the battery diagnostic system.

This script:
- Loads and preprocesses battery data
- Provides a CLI menu for user interaction
- Performs statistical analysis and visualization
- Generates LLM-based diagnostic insights
"""

from loader import load_all_data
from preprocessing import preprocess
from analysis import compute_group_summary
from prompts import comparison_prompt, single_battery_prompt
from llm_utils import call_llm
from visualization import plot_group, plot_box, plot_single_battery

DATA_FOLDER = "data"

# ===============================
# LOAD AND PREPROCESS DATA
# ===============================
df = load_all_data(DATA_FOLDER)
df = preprocess(df)

print("Data Loaded Successfully")

# ===============================
# MAIN INTERACTION LOOP
# ===============================
while True:

    print("\n==============================")
    print("1 - Temperature")
    print("2 - Load Type")
    print("3 - Load Level")
    print("4 - Single Battery")
    print("0 - Exit")
    print("==============================")

    choice = input("Select: ").strip()

    if choice == "0":
        print("Exiting program.")
        break

    # ===============================
    # GROUP ANALYSIS (OPTIONS 1–3)
    # ===============================
    if choice in ["1", "2", "3"]:

        # Map user input to grouping column and plot title
        group_map = {
            "1": ("temp_group", "Temperature Effect"),
            "2": ("load_type", "Load Type Comparison"),
            "3": ("load_level", "Load Level Effect")
        }

        group_col, title = group_map[choice]

        # -------- VISUALIZATION
        plot_group(df, group_col, title)
        plot_box(df, group_col)

        # -------- STATISTICAL ANALYSIS
        summary, best = compute_group_summary(df, group_col)

        print("\nSummary:")
        print(summary)

        print(f"\nKey Finding (data-driven): {best} shows fastest degradation.\n")

        # -------- PROMPT (ENFORCE CONSISTENCY WITH DATA)
        prompt = comparison_prompt(summary) + f"""

        IMPORTANT:
        - The fastest degradation group is: {best}
        - Your answer MUST match this result.
        """

        # -------- LLM RESPONSE
        output = call_llm(prompt)

        print("\nLLM Output:\n")
        print(output)

    # ===============================
    # SINGLE BATTERY ANALYSIS
    # ===============================
    elif choice == "4":

        files = df['file'].unique()

        print("\nAvailable Batteries:")
        for i, f in enumerate(files):
            print(f"{i}: {f}")

        try:
            idx = int(input("Select battery index: "))
            selected = files[idx]
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid index.")
            continue

        df_b = df[df['file'] == selected]

        if df_b.empty:
            print("No data available for selected battery.")
            continue

        # -------- VISUALIZATION (saves plot to outputs/)
        plot_single_battery(df_b, selected, save=True)

        # -------- BASIC METRICS
        initial = df_b['capacity'].iloc[0]
        final = df_b['capacity'].iloc[-1]
        fade = initial - final

        print("\nBattery Details:")
        print(f"Initial Capacity: {initial:.3f}")
        print(f"Final Capacity: {final:.3f}")
        print(f"Capacity Fade: {fade:.3f}")
        print(f"Total Cycles: {len(df_b)}")

        # -------- PROMPT GENERATION
        prompt = single_battery_prompt(
            selected,
            initial,
            final,
            fade,
            len(df_b),
            df_b['temp_group'].iloc[0],
            df_b['load_type'].iloc[0],
            df_b['load_level'].iloc[0]
        )

        # -------- LLM RESPONSE
        output = call_llm(prompt)

        print("\nLLM Output:\n")
        print(output)

    # ===============================
    # INVALID INPUT
    # ===============================
    else:
        print("Invalid option. Please try again.")