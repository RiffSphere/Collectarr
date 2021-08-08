#!/usr/bin/with-contenv bash
if [[ ! -f /config/collectarr.conf ]]; then
    echo "First run, cloning config into /config"
    mv /app/collectarr.conf.example /config
fi
if [[ ! -f /config/blacklist_collection.conf ]]; then
    mv /app/blacklist_collection.conf /config
fi
if [[ ! -f /config/blacklist_actor.conf ]]; then
    mv /app/blacklist_actor.conf /config
fi

chown -R root:root /config
chmod -R 777 /config
