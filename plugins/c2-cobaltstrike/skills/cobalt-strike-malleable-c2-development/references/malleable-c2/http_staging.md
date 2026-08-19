# HTTP Staging

Beacon is a staged payload. This means the payload is downloaded by a stager and injected into memory. Your http-get and http-post indicators will not take effect until Beacon is in memory on your target. Malleable C2’s http-stager block customizes the HTTP staging process.

```
http-stager {
     set uri_x86 "/get32.gif"; 
     set uri_x64 "/get64.gif";
```

The uri_x86 option sets the URI to download the x86 payload stage. The uri_x64 option sets the URI to download the x64 payload stage.

```
client {
     parameter "id" "1234"; 
     header "Cookie" "SomeValue";
}
```

The client keyword under the context of http-stager defines the client side of the HTTP transaction. Use the parameter keyword to add a parameter to the URI. Use the header keyword to add a header to the stager’s HTTP GET request.

```
server {
     header "Content-Type" "image/gif"; 
     output {
          prepend "GIF89a"; 
          print;
     }
}
```

The server keyword under the context of http-stager defines the server side of the HTTP transaction. The header keyword adds a server header to the server’s response. The output keyword under the server context of http-stager is a data transform to change the payload stage. This transform may only prepend and append strings to the stage. Use the print termination statement to close this output block.
