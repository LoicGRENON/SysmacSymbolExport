import csv

from sysmac_solution import SysmacSolution


def export_symbols_to_file(symbols, filename):
    symbols_data = [
        {
            'NAME': s.name,
            'DATATYPE': s.base_type,
            'COMMENT': s.comment,
            'RW': 'RW',
        }
        for s in symbols
    ]
    fieldnames = ['HOST', 'NAME', 'DATATYPE', 'ADDRESS', 'COMMENT', 'TAGLINK', 'RW', 'POU']
    # From Weintek documentation, the file should be in ANSI format. Hence, the CP1252 encoding
    with open(filename, 'w', newline='', encoding='cp1252') as f:
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(symbols_data)


if __name__ == '__main__':
    from pathlib import Path
    from sysmac_solution import get_solutions

    # Production path should be "C:\OMRON\Solution" (or other, depending on the installation directory maybe)
    solutions_path = Path("../assets/Solution")
    solutions = get_solutions(solutions_path)

    # TODO: Let the user to select which project to use
    # selected_project_uid = '665cc97e-6a2c-4394-a631-1a07a8708a92'
    selected_project_uid = '2e436523-51e9-41e3-9736-4d6ab40803c1'

    solution = SysmacSolution(solutions_path, selected_project_uid)
    symbols = solution.get_published_symbols()
    for s in symbols:
        print(f'{s.name} - {s.base_type} - {s.comment}')
    print(f'{len(symbols)} symbols found')

    export_symbols_to_file(symbols, '../assets/symbols.txt')
