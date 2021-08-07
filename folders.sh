#!/usr/bin/with-contenv bash
if [[ ! -f /config/rcm.default.conf ]]; then
    echo "First run, cloning config into /config"
    mv /app/collectarr.conf.example /config
fi

chown -R root:root /config
chmod -R 777 /config
