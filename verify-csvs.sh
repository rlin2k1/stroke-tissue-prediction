#!/bin/bash
# :: verify-csvs.sh
################################################
# Outputs the column count for each csv in a folder.
# Usage: verify-csvs.sh [directory-with-csvs]
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 1 June 2019

##############################################
# CONSTANTS
##############################################
readonly USAGE_MSG="~~~\n\
Outputs column count per csv file in a directory, with options to \
remove trailing columns, condense all into one output file, and more.\n\
~~~\n\
Usage: ./verify-csvs.sh -d <directory> [-n <count>] [-u]\n\
~~~\n"
readonly VALID_OPTS="Valid options:\n\
\tREQUIRED: -d <directory-name>: the name of the directory containing the CSV files.\n\
\tOPTIONAL: 
\t\t1) -n|--normalize <count>: normalize the CSVs to a particular column count (slicing off tail columns).
\t\t2) -c|--condense: condenses the CSVs contained within the directory into one file.
\t\t3) -f|--firstline <value>: if the condense option is specified, prepend the condensed file with <value> as the first line.
\t\t4) -i|--ignore <count>: ignore the first count lines from each .cvs if -c is specified.
\t\t5) -u|--usage: display this usage message.\n\
\n"

##############################################
# ARGUMENT PARSING
##############################################
count=0
normalize=false
condense=false
ignore_lines=false
first_line_set=false
FOLDER=false

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -u|--usage)
        printf "$USAGE_MSG"
        printf "$VALID_OPTS"
        exit 0
    ;;
    -n|--normalize)
        COL_LIM="$2"
        normalize=true
        echo "Will output normalized version of input files, limited to $2 columns. Files generated as norm_{original_name}.csv."
        shift # past argument
        shift # past value
    ;;
    -c|--condense)
        condense=true
        CONDENSED=$FOLDER/condensed.csv
        if [ $normalize != true ]; then
            echo "ERROR: cannot specify --condense without specifiying --normalize."
        fi
        echo "Will condense all normalized CSV files into one, titled condensed.csv."
        shift
    ;;
    -i|--ignore)
        if [ $condense != true ]; then
            echo "ERROR: cannot specify --ignore without specifiying --condense."
            exit 1
        fi
        IGNORE_COUNT=$(($2 + 1))
        ignore_lines=true
        echo "Will ignore the first $2 lines in each CSV when condensing."
        shift # past argument
        shift # past valuec
    ;;
    -f|--firstline)
        if [ $condense != true ]; then
            echo "ERROR: cannot specify --firstline without specifiying --condense."
            exit 1
        fi
        FIRST_LINE="$2"
        first_line_set=true
        echo "Will prepend $FIRST_LINE as the first line of the condensed CSV."
        shift # past argument
        shift # past value
    ;;
    -d|--directory) 
        if [[ $count -gt 1 ]];
        then
            echo "ERROR: only one directory may be specified."
            exit 1
        fi
        FOLDER="$2"
        if ! [ -d $FOLDER ]; then
            echo "ERROR: invalid directory specified."
            exit 1
        fi
        count=$((count + 1))
        shift
        shift
    ;;
    *) # unknown option
        echo "ERROR: unknown option specified."
        printf "$VALID_OPTS"
        exit 1
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

if [[ $count -lt 1 ]];
then
    echo "ERROR: no directory specified."
    exit 1
fi


if [ $condense = true ]; then
    if [ $first_line_set = true ]; then
        echo "$FIRST_LINE" > $CONDENSED
    else
        echo > $CONDENSED
    fi
fi

##############################################
# MAIN
##############################################


for file in $FOLDER/*.csv; do
    if [ $file != $CONDENSED ]; then
        col_count=$(cat $file | tail -n 1 | sed 's/[^,]//g' | wc -c)
        printf "$file: $col_count\n"
        if [ $normalize = true ]; then
            if [ $condense = true ]; then
                printf "\tAdding $file to $CONDENSED...\n"
                if [ $ignore_lines = true ]; then
                    cat $file | tail -n +$IGNORE_COUNT | cut -d, -f1-$COL_LIM >> $CONDENSED
                else
                    cut -d, -f1-$COL_LIM $file >> $CONDENSED
                fi
                printf "\tDone!\n"
            else
                printf "\tGenerating norm_$(basename $file)...\n"
                cut -d, -f1-$COL_LIM $file > $FOLDER/norm_$(basename $file)
                printf "\tDone!\n"
            fi
        fi
    fi
done
