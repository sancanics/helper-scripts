import re
import sys
import argparse

def extract_subdomain(url, pattern):
    """
    Extract the subdomain from a URL using a compiled regular expression pattern.
    """
    match = pattern.search(url)
    if match:
        return match.group(1)[:-1]  # Return subdomain without the trailing dot
    else:
        return None

if __name__ == '__main__':
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Extract subdomains from URLs using regular expressions.')
    parser.add_argument('-f', '--file', help='input file name')
    parser.add_argument('-o', '--output', help='output file name')

    # Parse command-line arguments
    args = parser.parse_args()

    # Compile regular expression pattern
    pattern = re.compile(r'^(?:https?://)?((?:[\w-]+\.)+)([\w\d]+\.[\w\d]+)')

    # Read URLs from file or stdin and extract subdomains
    if args.file:
        with open(args.file) as f:
            urls = f.read().splitlines()
        subdomains = {extract_subdomain(url, pattern) for url in urls}
    else:
        urls = [line.strip() for line in sys.stdin]
        subdomains = {extract_subdomain(url, pattern) for url in urls}

    # Remove None values from subdomains
    subdomains.discard(None)

    # Sort subdomains alphabetically
    sorted_subdomains = sorted(subdomains)

    # Write subdomains to output file, if specified
    if args.output:
        with open(args.output, 'w') as f:
            f.write('\n'.join(sorted_subdomains))
        print(f'Subdomains written to {args.output}')
    # Otherwise, print subdomains to stdout
    else:
        print(*sorted_subdomains, sep='\n')
        print('Subdomains extracted successfully')
