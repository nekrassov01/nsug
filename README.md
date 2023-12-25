# nsug

`nsug` means name suggestion. a tool for suggesting better names for variables, functions, and methods in code.

## Prerequisites

Setup environment variable: `OPENAI_API_KEY`

## Usage

```text
$ python3 nsug.py --help
usage: nsug.py [-h] [--code CODE] --name NAME [--max MAX]

nsug: a tool for suggesting better names for variables, functions, and methods in code.

options:
  -h, --help            show this help message and exit
  --code CODE, -c CODE  path to the code file
  --name NAME, -n NAME  name of the variable, function, or method to suggest names for
  --max MAX, -m MAX     maximum number of suggestions to return
```

## Example

```text
$ cat code.txt
func uniq(slice []string) []string {
	seen := make(map[string]struct{})
	res := make([]string, 0, len(slice))
	for _, s := range slice {
		if _, ok := seen[s]; !ok {
			seen[s] = struct{}{}
			res = append(res, s)
		}
	}
	return res
}
$ python3 nsug.py --name "seen"
uniqueStrings
distinctStrings
uniqueValues
distinctValues
filterDuplicates
```
