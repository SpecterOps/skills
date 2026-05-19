openScriptConsole

Open the Aggressor Script console.

#### Example

```
# Example using the dispatch_event aggressor script function
on ready {
   # Send the script console tab to the bottom of the cobalt strike window
   dispatch_event({
      $client = getAggressorClient();
      $tabMgr = [$client getTabManager];
      $console = openScriptConsole();
      [$tabMgr dockAppTab: $console];
   });
}```
