#!/usr/bin/env bash

rm *.dot

pyreverse -AS gloop
rm -rf diagrams/gloop
mkdir diagrams/gloop
mv *.dot diagrams/gloop/.

pyreverse -AS game
rm -rf diagrams/game
mkdir diagrams/game
mv *.dot diagrams/game/.

pyreverse -AS test
rm -rf diagrams/test
mkdir diagrams/test
mv *.dot diagrams/test/.