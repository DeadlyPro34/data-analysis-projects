import nbformat

with open('Football_Analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

filenames = [
    '01_top_teams.png',
    '02_most_successful_teams.png',
    '03_highest_scoring_teams.png',
    '04_best_defense.png',
    '05_home_advantage.png',
    '06_goals_over_time.png',
    '07_tournaments.png',
    '08_former_names.png',
    '09_top_scorers.png',
    '10_top_nations.png',
    '11_goal_types.png',
    '12_shootout_winners.png',
    '13_shootouts_over_time.png',
    '14_goal_distribution.png',
    '15_correlation.png'
]

file_idx = 0
for cell in nb.cells:
    if cell.cell_type == 'code':
        # Remove the big block of savefigs at the end
        if "plt.savefig('visualizations/02_most_successful_teams.png'" in cell.source:
            cell.source = "# Removed incorrect savefig block"
            continue
            
        if 'plt.show()' in cell.source:
            if "plt.savefig" not in cell.source and file_idx < len(filenames):
                # Insert savefig before show()
                parts = cell.source.split('plt.show()')
                new_source = parts[0] + f"plt.savefig('visualizations/{filenames[file_idx]}', dpi=300, bbox_inches='tight')\nplt.show()" + parts[1]
                cell.source = new_source
                file_idx += 1
            elif "plt.savefig" in cell.source:
                # Already there for the first one (01_top_teams.png)
                file_idx += 1

with open('Football_Analysis.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
    
print("Notebook patched successfully.")
