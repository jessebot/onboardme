# Random Notes

## apt notes

Thanks to Vaibhav for their solution [here](https://vskulkarni.wordpress.com/2011/10/07/gpg-error-httpppa-launchpad-net/) for when you get this error:
```bash
W: GPG error: http://ppa.launchpad.net lucid Release: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 4DEF31B9A9E345C0
```

It's *THIS* command: 

```bash
# 4DEF31B9A9E345C0 is your KEYID from the above error
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 4DEF31B9A9E345C0
```

## Misc

- [How does the vim write with sudo trick work?](https://stackoverflow.com/questions/2600783/how-does-the-vim-write-with-sudo-trick-work)
- Pretty view markdown: `pandoc README.md | lynx -stdin`
