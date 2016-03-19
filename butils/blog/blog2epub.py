#!/usr/bin/env python

import sys
import argparse
from ghost import *

'''
This is a executable python file, it should provide a shell API for operations regarding blog exporting features
'''
def main():

    DESCRIPTION='''
        This script will enable you to export your blog into epub. For now several blog engines are supported. Namely blogspot, wordpress, and ghost
    '''

    GHOST='ghost'
    BLOGGER='blogspot'
    WORDPRESS='wordpress'

    try:
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument('-b','--blog')
        parser.add_argument('-d','--database')
        parser.add_argument('-u','--url')
        parser.add_argument('-o','--output')

        args = parser.parse_args()

        if args.blog == 'ghost':
            if args.database != None and args.output != None:
                gh=GhostBlog(args.database)
                gh.toEpub(args.output)


        print args
    except Exception as ex:
        print ex.message
        sys.exit(2)

if __name__ == "__main__":
    main()
