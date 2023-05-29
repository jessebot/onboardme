echo ""
EXTRA_GROUPS=""
if [ ! -z $DEFAULT ]; then EXTRA_GROUPS+=" -g default"; fi
if [ ! -z $DATA_SCIENCE ]; then EXTRA_GROUPS+=" -g data_science"; fi
if [ ! -z $DEVOPS ]; then EXTRA_GROUPS+=" -g devops"; fi
if [ ! -z $MAIL ]; then EXTRA_GROUPS+=" -g mail"; fi
if [ ! -z $MUSIC ]; then EXTRA_GROUPS+=" -g music"; fi

obm_cmd="onboardme --no_upgrade --log_level debug$EXTRA_GROUPS"
echo "running onboardme command now: $obm_cmd"
eval $obm_cmd
echo "finished running onboardme"

echo "moving fastfetch config into place"
mkdir ${XDG_CONFIG_HOME}/fastfetch
mv /tmp/config.conf ${XDG_CONFIG_HOME}/fastfetch/config.conf
