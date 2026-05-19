bjoblog

Publishes a job output message to the Beacon transcript. Its primary purpose is to be used in the post-execution job's callback function.

#### Arguments:

`$1` - the id for the beacon to post to.

`$2` - the related job id.

`$3` - the test to post.

#### Example:

```
beacon_execute_postex_job($bid, $null, $dll_content, $args, {
    local('$bid $result %info $type');
    ($bid, $result, %info) = @_;
    $type = %info["type"] ;
    $jid = %info["jid"] ;
    if ($type eq "error") {
        bjoberror($bid, $jid, "[postex-cb: $+ $type $+ ]: " . $result);
    }
    else {
        bjoblog($bid, $jid, "[postex-cb: $+ $type $+ ]: " . $result);
    }
});```

