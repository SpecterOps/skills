bjob_send_data

Sends data to the DLL over the named pipe. 

NOTE: The Postex Kit DLL must read any data on the pipe before Beacon can write any additional data to it. See *Bi-Directional Comms* and *Callbacks* for examples.#### Arguments

$1 - the Beacon id

$2 - the Job id

$3 - the data to send

#### Example

```
bjob_send_data($beacon_id, $job_id, $data);```

