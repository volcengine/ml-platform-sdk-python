#!/bin/bash

set -e

if ! type pylint &> /dev/null ; then
  echo "pylint is not found, please install it by \`pip3 install pylint\`"
  exit 1
fi
if ! type yapf &> /dev/null ; then
  echo "yapf is not found, please install it by \`pip3 install yapf\`"
  exit 1
fi

# Ignore deleted file
if [ "$1" = "precommit" ]; then
  changed_files=$(git diff --cached --name-only --diff-filter=ACM)
else
  # $2: latest commit SHA in source branch
  # $3: latest commit SHA in target branch
  changed_files=$(git diff --name-only --diff-filter=ACM "$2" "$3")
fi

for file in ${changed_files}; do
  flag=0
  for (( i=0;i<${#BLACKLIST_FOLDER[@]};i++ )) do
    if [[ ${file} == ${BLACKLIST_FOLDER[i]}*.py ]]; then
      flag=1
      break
    fi
  done
  if [ ${flag} -eq 1 ]; then
    continue
  fi
  if [ "${file##*.}" != "py" ]; then
    continue
  fi
	
  echo "Checking format and style for: $file"
  yapf -dpr "$file"
  pylint "$file"
done
