#!/bin/bash

set -e

## Ignore deleted file
#if [ "$1" = "precommit" ]; then
#  changed_files=$(git diff --cached --name-only --diff-filter=ACM)
#else
#  # $2: latest commit SHA in source branch
#  # $3: latest commit SHA in target branch
#  changed_files=$(git diff --name-only --diff-filter=ACM "$2" "$3")
#fi
all_files=$(find tests samples volcengine_ml_platform -name "*.py")

for file in ${all_files}; do
  if [ ! -f "${file}" ]; then
    continue
  fi
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
	
  echo "Checking yapf for: $file"
  yapf -i "$file"
done
