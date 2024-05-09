from rich.table import Table
from rich.console import Console

def _display_data(data):
    console = Console()

    display_order = [
        'name',
        'hash',
        'size',
        'pieces',
        'creation',
        'comment',
        'private',
        'trackers',
        'webseeds',
        'files'
    ]

    key_mapping = {
        'trackers': 'Tracker URL(s)',
        'webseeds': 'Webseed URL(s)'
    }

    main_table = Table(show_header=False, box=None)

    for key in display_order:
        if key in data:
            display_key = key_mapping.get(key, key.capitalize())
            value = data[key]

            if key == 'files':
                sub_table = Table(show_header=False, expand=True)
                sub_table.add_column("File Path")
                sub_table.add_column("File Size")

                for file_data in value:
                    sub_table.add_row(f"• {file_data['path']}", file_data['size'])

                main_table.add_row(f"[bold]{display_key}[/bold]", sub_table)
            else:
                if isinstance(value, list):
                    value = "\n".join(f"• {v}" for v in value)
                elif isinstance(value, dict):
                    if key == 'creation':
                        value = f"{value['date']} by {value['tool']}"
                    elif key == 'pieces':
                        value = f"{value['total']} of length {value['length']} (last piece {value['last_piece_size']})"
                    else:
                        value = "\n".join(f"{k}: {v}" for k, v in value.items())
                elif key == 'private':
                    value = 'True' if str(value) == '1' else 'False'

                main_table.add_row(f"[bold]{display_key}[/bold]", str(value))

    console.print(main_table)
