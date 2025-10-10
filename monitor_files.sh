#!/bin/bash
echo "Monitoring file changes..."
inotifywait -m -r -e create,modify,delete /opt/imediatoseguros-rpa/temp/ /opt/imediatoseguros-rpa/rpa_data/ 2>/dev/null | while read path action file; do
    echo "$(date): $action $path$file"
done






















