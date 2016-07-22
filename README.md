# gedit-fancychars
Fancy (unicode) character plugin for gedit3

This TeXmacs inspired plugin generates unicode symbols as you type by catching key sequences, or by pressing `TAB`.

## Requirements

This plugin currently only works with Gedit 3.x.

## Usage

The plugin works in two ways:

### Using Tab

Pressing `TAB` will remove a number of preceeding characters and type in a replacement instead, providing the preceeding characters are found in the **cycles.txt** file in the plugin's directory. Pressing `TAB` multiple times will cycle through all the available replacements before return to the original character.

#### Some examples

* Typing `d` followed by `TAB` results in a lower case Greek delta character `δ`. Pressing `TAB` again returns it to `d`.
* Similary, typing `D` followed by `TAB` results in an upper case `Δ`. Pressing `TAB` returns it to `D`. All the Greek lower case and upper case letters are available.
* Some characters have multiple substitutions, e.g. `<` `TAB` becomes, `∈`. Another `TAB` changes it to `⊂`. Yet one more `TAB` changes it `〈`. Pressing `TAB` again changes it back to `<`.

### Using Character Combinations

The plugin will also replace sequences of characters, configured by the **combos.txt** file in the plugin's directory. The replacement is immediate after the characters are typed. The replacement character can be combined with more characters by continuing to type, or cycled through replacements using `TAB` as above. The original sequence is always one of the `TAB`-able alternatives, allowing the original sequence to be restored when the replacement was not required.

### Some examples

* Typing `<` followed by `=` replaces the two characters with `⩽`. Pressing `TAB` replaces that with `≤`. Pressing `TAB` again changes it to `⊆`. The next `TAB` restores the original `<=`.
* As above, typing `<` `TAB` becomes `∈`. Typing `/` directly after replaces it with `∉`.

## Installation

To install this plugin, copy the files **fancychars.plugin** and the directory **fancychars** into **~/.local/share/gedit/plugins** and enable the plugin from the preferences dialog.

### Configuration

The full set of replacement characters can be found in the files **cycles.txt** and **combos.txt** in the **fancychars** directory. To ease configuration, the plugin adds a menu item *Fancy Chars Editor* to the main cog menu which simply opens these two files for editing. The plugin automatically reparses these files whenever they change on disk.

### TODO

- [ ] Configure the plugin to work on specific file types.
- [ ] Allow the plugin to be enabled / disabled each view.
- [ ] Use different cycles / combos for different file types.


