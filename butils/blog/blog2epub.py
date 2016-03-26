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

        parser.add_argument('-b','--blog',
            help='The blog provider name, for now possible values are <ghost>, <blogger> and <wordpress>')

        parser.add_argument('-d','--database',
            help='Use this parameter only when dealing with blogs based on ghost engine to specify the path for the sqlite database')

        parser.add_argument('-u','--url', help='This receives de url of the blog, use this for blogs based on blogger and wordpress')

        parser.add_argument('-a','--authors',
            help='List of authors. You should use a comma to split the several entries. \
        For example if your list has two authors namely Steven John and Charles Pryo you should pass them like this -a \
        "Charles Pryo,Steven John" and don\'t forget the " in the beginning and end of the list')

        parser.add_argument('-o','--output',
            help='This is the name that will be assigned for the file that will be generated.')

        parser.add_argument('-n','--name',
            help='This is the name of the blog, it is mandatory for blogger and worpress but not used in ghost blogs\
            since it is auto detected in this last case. It will be the field used for the title of the ebook in the\
            final output file'
        )

        args = parser.parse_args()

        if args.blog == 'ghost':
            if args.database != None and args.output != None:
                gh=GhostBlog(args.database)
                gh.toEpub(args.output)

        #Process blogger request
        if args.blog == 'blogger':
            print "Process blogger"

        #Process wordpress request
        if args.blog == 'wordpress':
            print "process wordpress"


        print args
    except Exception as ex:
        print ex.message
        sys.exit(2)

if __name__ == "__main__":
    main()
