# A Beacon HTTP Transaction Walk-through

To put all of this together, it helps to know what a Beacon transaction looks like and which data is sent with each request.

A transaction starts when a Beacon makes an HTTP GET request to Cobalt Strike’s web server. At this time, Beacon must send metadata that contains information about the compromised system.

> Session metadata is an encrypted blob of data. Without encoding, it is not suitable for transport in a header or URI parameter. Always apply a base64, base64url, or netbios statement to encode your metadata.

Cobalt Strike’s web server responds to this HTTP GET with tasks that the Beacon must execute. These tasks are, initially, sent as one encrypted binary blob. You may transform this information with the output keyword under the server context of http-get.

As Beacon executes its tasks, it accumulates output. After all tasks are complete, Beacon checks if there is output to send. If there is no output, Beacon goes to sleep. If there is output, Beacon initiates an HTTP POST transaction.

The HTTP POST request must contain a session id in a URI parameter or header. Cobalt Strike uses this information to associate the output with the right session. The posted content is, initially, an encrypted binary blob. You may transform this information with the output keyword under the client context of http-post.

Cobalt Strike’s web server may respond to an HTTP POST with anything it likes. Beacon does not consume or use this information. You may specify the output of HTTP POST with the output block under the server context of http-post.

> While http-get uses GET by default and http-post uses POST by default, you’re not stuck with these options. Use the verb option to change these defaults. There’s a lot of flexibility here.

This table summarizes these keywords and the data they send:

| Request     | Component | Block    | Data                  |
| ----------- | --------- | -------- | --------------------- |
| http-get    | client    | metadata | Session metadata      |
| http-get    | server    | output   | Beacon’s tasks        |
| http-post   | client    | id       | Session ID            |
| http-post   | client    | output   | Beacon’s responses    |
| http-post   | server    | output   | Empty                 |
| http-stager | server    | output   | Encoded payload stage |
