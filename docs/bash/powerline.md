# Powerline - a status line for your terminal
Powerline has plugins common shells, to create beautiful prompts for shells such as BASH or ZSH, but it can also work with vim, tmux, and other apps.

Here's an example of my personal powerline setup. (You can look at the actual config files [here](https://github.com/jessebot/onboardme/tree/main/configs/dot_files/.config/powerline) )

<img src="./ssh_powerline_example.png">

Above you can see I use a multiline prompt in order to have space for a full command line interface, as well as useful data in the prompt, like current working directory. The line grows and shrinks depending on external factors like if I'm connected to a k8s cluster and I'm in a special namespace, or if the last command I ran failed. It's also useful for git status. I utilize this to cut down on typing things like `pwd`, `hostname`, `git status`, `echo $?`, and `date` constantly, because my RSI is terrible.

<img src="./git_powerline_example.png">
