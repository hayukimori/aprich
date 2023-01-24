# aprich

Discord rich presence for local players that uses the `playerctl` API.

## Installation 

### *for unix-like systems*
1. First of all, install the `pypresence` dependencie: **`python -m pip install pypresence`**
2. Clone this repo: **`git clone https://github.com/hayukimori/aprich`**
3. Install/update by copping the main file to the bin directory: **`cp aprich/main.py ~/.local/bin/aprich`**
4. Give *execution permition* to that file wiht: **`chmod +x ~/.local/bin/aprich`**

Hey, heres a snippet to make your work eseaier 😊. Just copy and paste it in youre terminal emulator:
```bash
python -m pip install pypresence
git clone https://github.com/hayukimori/aprich
cp aprich/main.py ~/.local/bin/aprich
chmod +x ~/.local/bin/aprich
```

Unninstall by removing the copied file with:
```bash
rm ~/.local/bin/aprich
```
> Maybe you also want to remove the `pypresence` library too with **`python -m pip uninstall pypresence`**

## Usage
After installed on `~/.local/bin/`, the usage will be easier, just run aprich on terminal, like this
```bash
$ aprich
```

Some arguments have been added, worth a look with `aprich --help`
**Explanation of arguments**
- `--enable-github-button` or `-b`: This option shows a button that takes you to this repository
- `--image` or `-i`: In this option you can change to any of the default images


**Available images**

- `3dhp`: A pink headphone.
- `3dhp_black`: A black/gray headphone (to combine with profiles without Nitro) ( default )
- `cardinal_anime`: Default bot's profile picture
