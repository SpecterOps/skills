# HTTP Server Configuration

The http-config block has influence over all HTTP responses served by Cobalt Strike’s web server. Here, you may specify additional HTTP headers and the HTTP header order.

```
http-config {
     set headers "Date, Server, Content-Length, Keep-Alive, 
                    Connection, Content-Type"; 
     header "Server" "Apache";
     header "Keep-Alive" "timeout=5, max=100";    
     header "Connection" "Keep-Alive";
     set trust_x_forwarded_for "true";
     set block_useragents "curl*,lynx*,wget*";
}
```

set headers - This option specifies the order these HTTP headers are delivered in an HTTP response. Any headers not in this list are added to the end.

header - This keyword adds a header value to each of Cobalt Strike’s HTTP responses. If the header value is already defined in a response, this value is ignored.

set trust_x_forwarded_for - This option decides if Cobalt Strike uses the X-Forwarded-For HTTP header to determine the remote address of a request. Use this option if your Cobalt Strike server is behind an HTTP redirector.

block_useragents and allow_useragents - These options configure a list of user agents that are blocked or allowed with a 404 response. By default, requests from user agents that start with curl, lynx, or wget are all blocked. If both are specified, block_useragents will take precedence over allow_useragents. The option value supports a string of comma separated values. Values support simple generics:

| Example                   | Description                                                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| not specified             | Use the default value (`curl*`,`lynx*`,`wget*`). Block requests from user agents starting with curl, lynx, or wget. |
| blank (block_useragents)  | No user agents are blocked.                                                                                         |
| blank (allow user_agents) | All user agents are allowed.                                                                                        |
| `something`               | Block/Allow requests with useragent equal `'something'`.                                                            |
| `something*`              | Block/Allow requests with useragent starting with `'something'`.                                                    |
| `*something`              | Block/Allow requests with useragent ending with `'something'`.                                                      |
| `*something*`             | Block/Allow requests with useragent containing `'something'`.                                                       |
