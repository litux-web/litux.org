#!/bin/bash

[ -d .venv ] && source .venv/bin/activate

#!/bin/bash

touch -t 200001010000 .touch

while true ; do
	while [ "x$(find data templates src -type f -a -newer .touch)" = "x" ] ; do
		sleep 1
	done
    touch .touch2
    sleep 1

    echo [START] $(date)
    python3 src/generate.py -f
    echo [DONE] $(date)

    [ -r .touch2 ] && mv -f .touch2 .touch
done

