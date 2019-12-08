#!/bin/bash

git status
echo "This is what changes"
git add .
git commit -m $1
git push origin master