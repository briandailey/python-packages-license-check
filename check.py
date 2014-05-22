#!/usr/bin/env python
import pkg_resources
import argparse
import sys

from pip.util import get_installed_distributions


def main():
    parser = argparse.ArgumentParser(description="Read all installed packages from sys.path and list licenses.")
    args = parser.parse_args()

    for installed_distribution in get_installed_distributions():
        found_license = False
        try:
            for line in installed_distribution.get_metadata_lines('PKG-INFO'):
                if 'License:' in line:
                    (k, v) = line.split(': ', 1)
                    if k == "License":
                        sys.stdout.write("{project_name}: {license}\n".format(
                            project_name=installed_distribution.project_name,
                            license=v))
                        found_license = True
        except IOError as e:
            # usually because the PKG-INFO file was not found.
            sys.stderr.write("Failed to get license information for {project_name}\n".format(
                project_name=installed_distribution.project_name))
            sys.stderr.write(str(e) + "\n")
        if not found_license:
            sys.stdout.write("{project_name}: Found no license information.\n".format(
                project_name=installed_distribution.project_name))

if __name__ == "__main__":
    main()
