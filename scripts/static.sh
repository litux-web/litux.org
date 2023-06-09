#!/bin/bash

if [ -d "litux.org" ] ; then
    git submodule update --remote
    mkdir -p docs/css docs/js
    for i in $(cd litux.org ; ls \
            scripts/static.sh \
            scripts/integrity \
            docs/robots.txt \
            docs/css/*.css \
            docs/js/*.js \
	    templates/*.html \
        ) ; do
        if [ ! -r "$i" ] ; then
            cp -v "litux.org/$i" "$i"
        else
            diff -q "litux.org/$i" "$i" || \
                cp -v "litux.org/$i" "$i"
        fi
    done
fi
