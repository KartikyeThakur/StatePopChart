import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

# Load the Excel file (adjust path as needed)
df = pd.read_excel(r'C:\Users\KARTIKYE\Downloads\state_population.xlsx', skiprows=2)

# Initial exploration and cleaning
print(df.head())  # Check the first few rows
print(df.columns)  # Print column names to verify

# Remove rows with all NaN values (if any)
df.dropna(how='all', inplace=True)

# Convert numeric columns to appropriate data types and handle missing values
numeric_columns = ['Total Population', 'Total Male Population', 'Total Female Population',
                   'Total Population.1', 'Total Male Population.1', 'Total Female Population.1',
                   'Total Population.2', 'Total Male Population.2', 'Total Female Population.2',
                   'Total Population.3', 'Total Male Population.3', 'Female Population']

# Adjust column names if needed
df[numeric_columns] = df[numeric_columns].apply(lambda x: x.astype(str).str.replace(',', '').astype(float))

# Validate data
for i in range(4):  # Adjust the range to include all years (0, 1, 2, 3 for 1991, 2001, 2011, 2021)
    total_pop_col = f'Total Population.{i}' if i > 0 else 'Total Population'
    male_pop_col = f'Total Male Population.{i}' if i > 0 else 'Total Male Population'
    female_pop_col = f'Total Female Population.{i}' if i > 0 else 'Total Female Population'

    # Check if columns exist before filtering
    if total_pop_col in df.columns and male_pop_col in df.columns:
        df = df[df[total_pop_col] >= df[male_pop_col]]
    if total_pop_col in df.columns and female_pop_col in df.columns:
        df = df[df[total_pop_col] >= df[female_pop_col]]

# Define the years available in your dataset for plotting
years = ['1991', '2001', '2011', '2021']  # Update with actual years in your dataset

# Define colors for each population category
color_map = {
    'Total Population': 'blue',
    'Total Male Population': 'green',
    'Total Female Population': 'red'
}

# Group by State/UT, sort alphabetically, and iterate through each group to create separate plots
for state, state_df in df.groupby('State/UT'):
    # Sort the state data alphabetically
    state_df = state_df.sort_values(by='State/UT')

    # Create a separate plot for each state
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot Total Population, Total Male Population, and Total Female Population for each year
    bar_width = 0.2
    r1 = range(len(years))

    for i, year in enumerate(years):
        total_pop_col = f'Total Population.{i}' if i > 0 else 'Total Population'
        male_pop_col = f'Total Male Population.{i}' if i > 0 else 'Total Male Population'
        female_pop_col = f'Total Female Population.{i}' if i > 0 else 'Total Female Population'

        # Check if the columns exist before accessing
        if (total_pop_col in state_df.columns and male_pop_col in state_df.columns
                and female_pop_col in state_df.columns):
            total_pop = state_df[total_pop_col].values[0]
            male_pop = state_df[male_pop_col].values[0]
            female_pop = state_df[female_pop_col].values[0]

            # Plot bars with labels for each bar set
            bar1 = ax.bar(i - bar_width, total_pop, color=color_map['Total Population'], width=bar_width, alpha=0.7,
                          label='Total Pop' if i == 0 else "")
            bar2 = ax.bar(i, male_pop, color=color_map['Total Male Population'], width=bar_width, alpha=0.7,
                          label='Male Pop' if i == 0 else "")
            bar3 = ax.bar(i + bar_width, female_pop, color=color_map['Total Female Population'], width=bar_width,
                          alpha=0.7, label='Female Pop' if i == 0 else "")

            # Add cursor annotation for each bar
            mplcursors.cursor(bar1, hover=True).connect("add", lambda sel: sel.annotation.set_text(
                f'Total Pop: {sel.target[1]:.0f}'))
            mplcursors.cursor(bar2, hover=True).connect("add", lambda sel: sel.annotation.set_text(
                f'Male Pop: {sel.target[1]:.0f}'))
            mplcursors.cursor(bar3, hover=True).connect("add", lambda sel: sel.annotation.set_text(
                f'Female Pop: {sel.target[1]:.0f}'))

            # Add note if population is zero for any category
            if total_pop == 0:
                ax.text(i - bar_width, total_pop, 'State not found', ha='center', va='bottom', fontsize=8,
                        color='black', weight='bold')
            if male_pop == 0:
                ax.text(i, male_pop, 'State not found', ha='center', va='bottom', fontsize=8,
                        color='black', weight='bold')
            if female_pop == 0:
                ax.text(i + bar_width, female_pop, 'State not found', ha='center', va='bottom', fontsize=8,
                        color='black', weight='bold')

    # Customize plot
    ax.set_xlabel('Year')
    ax.set_ylabel('Population')
    ax.set_title(f'Population Distribution in {state}')
    ax.set_xticks(range(len(years)))
    ax.set_xticklabels(years)

    # Add grid, rotate x-ticks for better readability
    ax.grid(True)
    plt.xticks(rotation=45)

    # Add more details to enhance readability
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: '{:,.0f}'.format(x)))  # Format y-axis labels with comma separators
    ax.axhline(0, color='black', linewidth=0.5)  # Add horizontal line at y=0
    ax.spines['top'].set_visible(False)  # Remove top border
    ax.spines['right'].set_visible(False)  # Remove right border

    # Create legend only once for each type of bar
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1))

    # Show plot for the current state
    plt.tight_layout()
    plt.show()
