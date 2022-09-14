# Driagrams for this script
This is heavily under construction

# needs own chart
subproc(command="", error_ok=False, suppress_output=False)

# boilerplate
print_head(status="")

# first
Grab OS, home directory, and script directory
parse_args()
parse_local_configs()
hard_link_dot_files(delete=False,
run_installers(installers=['brew'], pkg_groups=['default'])
configure_vim()

# middle
install_fonts()

# optional
configure_ssh()
configure_firewall(remote_hosts=[])
map_caps_to_control()
configure_firefox()

# last
configure_terminal(OS='darwin')
setup_nix_groups()
configure_feeds()


graph TD
    A[onboardme.py] -->|"main()"| B(parse_args)
    B --> C{if fab:fa-apple}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]

graph TD
    A[onboardme.py] -->|main| B()
    B --> C{Let me think}
    C -->|One| D[Laptop]
    C -->|Two| E[iPhone]
    C -->|Three| F[fa:fa-car Car]
