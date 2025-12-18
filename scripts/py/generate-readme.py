import sys
sys.pycache_prefix='C:/__pycache__'
from snippet_expander import expand_snippets

if __name__ == "__main__":
    args = sys.argv[1:]

    add_line_numbers = True
    if "--no-lines" in args:
        add_line_numbers = False
        args.remove("--no-lines")

    if len(args) == 0:
        expand_snippets(add_line_numbers=add_line_numbers)
    elif len(args) == 1:
        expand_snippets(path_dir=args[0], add_line_numbers=add_line_numbers)
    elif len(args) >= 2:
        expand_snippets(path_dir=args[0], blanks_dir=args[1], add_line_numbers=add_line_numbers)
