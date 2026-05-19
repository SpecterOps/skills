sync_download

Sync a downloaded file (View -> Downloads) to a local path.

#### Arguments

`$1` - the remote path to the file to sync. See &downloads

`$2` - where to save the file locally

`$3` - (optional) a callback function to execute when download is synced. The first argument to this function is the local path of the downloaded file.

#### Example

```
# sync all downloads
command ga {
   local('$download $lpath $name $count');
   foreach $count => $download (downloads()) {
      ($lpath, $name) = values($download, @("lpath", "name"));
   
      sync_download($lpath, script_resource("file $+ .$count"), lambda({ 
         println("Downloaded $1 [ $+ $name $+ ]"); 
      }, \$name));
   }
}```

