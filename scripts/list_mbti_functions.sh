#!/bin/bash

# Get script directory and project root (adjust if needed)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# If no arguments given, use all 16 MBTI types
if [ "$#" -eq 0 ]; then
  mbti_types=(
    ISTJ ISFJ INFJ INTJ
    ISTP ISFP INFP INTP
    ESTP ESFP ENFP ENTP
    ESTJ ESFJ ENFJ ENTJ
  )
else
  # Use types passed as arguments (convert to uppercase)
  mbti_types=()
  for arg in "$@"; do
    mbti_types+=("$(echo "$arg" | tr '[:lower:]' '[:upper:]')")
  done
fi

echo "Listing cognitive functions for MBTI types: ${mbti_types[*]}"
echo "----------------------------------------------------------"

for type in "${mbti_types[@]}"
do
  echo "MBTI Type: $type"
  # Run analyze command from project root
  output=$(cd "$PROJECT_ROOT" && python3 eidon.py analyze --type "$type" --functions ego subconscious unconscious superego 2>/dev/null)

  if [[ -z "$output" ]]; then
    echo "  ERROR: No output for $type"
  else
    # Indent output lines for readability
    echo "$output" | sed 's/^/  /'
  fi

  echo "----------------------------------------------------------"
done

