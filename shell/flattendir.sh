# via http://stackoverflow.com/a/20800032/682915

target="/tmp/target"
find . -type f | while read line; do
  outbn="$(basename "$line")"
  while true; do
    if [[ -e "$target/$outbn" ]]; then
      outbn="z-$outbn"
    else
      break
    fi
  done
  cp "$line" "$target/$outbn"
done
