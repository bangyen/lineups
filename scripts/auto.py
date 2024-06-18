import src.generate as generate
import scripts.main as main
import argparse
import shutil
import os

def header(fmt, val):
    new = f'=== {fmt} ==='
    print(new.format(val))


def default(parser, name, value):
    """
    Adds a default argument to the given
    parser with short and long options.
    """
    parser.add_argument(
        f'-{name[0]}',
        f'--{name}'  ,
        default=value
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Add default arguments
    default(parser, 'json'  , 'scripts/json.zlib')
    default(parser, 'input' , 'data'             )
    default(parser, 'output', 'data/done'        )
    default(parser, 'backup', 'backup'           )

    args   = parser.parse_args()
    folder = args.input

    # Iterate over files in the input folder
    for file in os.listdir(folder):
        num  = len(os.listdir(args.backup))
        back = f'{args.backup}/backup_{num}.zlib'

        # Get the file extension and path
        ext  = os.path.splitext(file)[1]
        path = f'{folder}/{file}'

        if ext == '.html':
            func = main.html
        elif ext == '.txt':
            func = main.text
        else:
            continue

        # Parse the file and add to the database
        header('Current file: {}', file)
        generate.wrap([path], func, True, True)

        # Create a backup and archive the processed file
        header('Creating backup_{}.zlib', num)
        shutil.copy(args.json, back)
        shutil.move(path, args.output)
