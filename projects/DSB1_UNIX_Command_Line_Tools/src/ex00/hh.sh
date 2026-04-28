VAR1="$(jq --version)"


if [ "$VAR1" != "jq-1.7.1" ] && \
   [ "$VAR1" != "jq-1.8.1" ] && \
   [ "$VAR1" != "jq-1.8.0" ] && \
   [ "$VAR1" != "jq-1.7" ]; then
    mkdir ~/bin
    curl -L https://github.com/jqlang/jq/releases/download/jq-1.7.1/jq-macos-amd64 -o ~/bin/jq
    chmod +x ~/bin/jq
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
fi

job="$1"
curl -s --get "https://api.hh.ru/vacancies" \
     --data-urlencode "text=$job" \
     --data-urlencode "per_page=20" \
     | jq '.items' > hh.json