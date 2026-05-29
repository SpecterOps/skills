addTab

Create a tab to display a GUI object.

#### Arguments

`$1` - the title of the tab

`$2` - a GUI object. A GUI object is one that is an instance of **javax.swing.JComponent**.

`$3` - a tooltip to display when a user hovers over this tab.

#### Example

```
$label = [new javax.swing.JLabel: "Hello World"];
addTab("Hello!", $label, "this is an example");```
