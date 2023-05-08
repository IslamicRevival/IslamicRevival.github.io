#!/usr/bin/env python3

import markdown
import os
import sys

# Get the directory name from the command line
directory = sys.argv[1]

# Get a list of all the Markdown files in the directory
markdown_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.md')]

# For each Markdown file, fix errors, missing tags, and optimize the file
for markdown_file in markdown_files:

    # Read the file contents
    with open(markdown_file, 'r') as f:
        content = f.read()

    # Convert the content to Markdown
    markdown_content = markdown.markdown(content, safe=True)

    # Check for missing tags
    missing_tags = []
    for processor in markdown.blockprocessors:
        if processor.name not in markdown_content:
            missing_tags.append(processor.name)

    # Print a warning if any missing tags are found
    if missing_tags:
        print('The following tags are missing in {}: {}'.format(markdown_file, missing_tags))

    # Optimize the Markdown
    optimized_content = markdown.optimize(markdown_content)

    # Write the optimized content to a file
    with open(markdown_file, 'w') as f:
        f.write(optimized_content)