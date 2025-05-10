#!/bin/bash

# Get the directory of this script (tests/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Project root is parent directory of tests/
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

mbti_types=(
  ISTJ ISFJ INFJ INTJ
  ISTP ISFP INFP INTP
  ESTP ESFP ENFP ENTP
  ESTJ ESFJ ENFJ ENTJ
)

echo "Testing MBTI <-> Cognitive Stack consistency..."

failures=0

for type in "${mbti_types[@]}"
do
  echo "Testing $type..."

  # Run analyze from project root
  ego_line=$(cd "$PROJECT_ROOT" && python3 eidon.py analyze --type "$type" --functions ego 2>/dev/null | grep '^Ego:')

  if [[ -z "$ego_line" ]]; then
    echo "  ERROR: No ego stack returned for $type"
    ((failures++))
    continue
  fi

  stack_str=${ego_line#Ego: }
  stack_args=$(echo "$stack_str" | tr '-' ' ')

  # Run infer from project root
  inferred=$(cd "$PROJECT_ROOT" && python3 eidon.py infer --stack $stack_args 2>/dev/null | grep '^MBTI Type:' | awk '{print $3}')

  if [[ "$inferred" == "$type" ]]; then
    echo "  PASS: inferred $inferred matches original $type"
  else
    echo "  FAIL: inferred $inferred does NOT match original $type"
    ((failures++))
  fi
done

echo
if ((failures == 0)); then
  echo "All tests passed successfully!"
else
  echo "$failures test(s) failed."
fi

