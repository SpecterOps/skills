addVisualization

Register a visualization with Cobalt Strike.

#### Arguments

`$1` - the name of the visualization

`$2` - a **javax.swing.JComponent** object

#### Example

```
$label = [new javax.swing.JLabel: "Hello World!"];
addVisualization("Hello World", $label);```

See also&showVisualization
