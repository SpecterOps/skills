# HTTP Host Profiles

Host Profiles is used to define HTTP characteristics (uri, headers, and parameters) that will be used for the HTTP/HTTPS communication traffic for a specific host name. Host Profiles is optional. Host Profiles can be defined for multiple host names.

## About Dynamic Data

Some fields in http-host-profiles group support a dynamic value syntax. Beacons will randomly select one of the optional values in the specified dynamic syntax. Dynamic syntax is wrapped by square brackets with values separated by "|".

| Feature                                                                | Example                                                        | Resolves to                                                                    |
| ---------------------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Dynamic syntax can be an entire value.                                 | `[example.abc\|sample.def\|demo.ghi]`                          | `example.abc`<br>`sample.def`<br>`demo.ghi`                                    |
| Dynamic syntax can be embedded in static text.                         | `prefix/[a\|b]/suffix`                                         | `prefix/a/suffix`<br>`prefix/b/suffix`                                         |
| Dynamic syntax can have one or more blank options as a selected value. | `abc/folder[1\|\|3\|]/xyz`                                     | `abc/folder1/xyz`<br>`abc/folder/xyz`<br>`abc/folder3/xyz`<br>`abc/folder/xyz` |
| Dynamic syntax can have multiple dynamic items.                        | `[abc\|xyz]/[123\|456]/`<br>`[index.html\|hello.js\|home.jsp]` |                                                                                |

```
http-host-profiles {
  profile {
      set             host-name                   "one.ytrewq.com"; 
      http-get {
          set         uri                         "/[a|b|c|d]/ytrewq/get.js";
          header      "ytrewq-header-[a|b|c]"     "static-value";
          parameter   "ytrewq-parameter"          "value-[x|y|z]";
          parameter   "ytrewq-[a|b|c]"            "value-[x|y|z]";
      ## Example of param name that will be dropped when it resolves as blank
          parameter   "[p1|||p4]"                 "[a|b|c]";  
      }
      http-post {
          set         uri   "/[a|b|c|d]/ytrewq/[post1|post2|post3|post4].js";
          header      "ytrewq-header-[a|b|c]"     "static-value";
          parameter   "ytrewq-parameter"          "value-[x|y|z]"; 
          parameter   "ytrewq-[a|b|c]"            "value-[x|y|z]";
          parameter   "[p1|||p4]"                 "[a|b|c]";
      }
  }
  profile {
      set             host-name        "two.ytrewq.com";
      http-get {
          set         uri              "/ytrewq/get/[2|two|dos]/[a|b|c].js";
      }
      http-post {
          set         uri              "/ytrewq/post/[2|two|dos]/[a|b|c].js";
      }
  }
}
```

The settings are:

| Field     | Description                                                                                                                                                                                                                                                                                                                                                                           |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| host-name | The host-name field is a fixed string that links the Host Profile to matching **HTTP Hosts** field on the HTTP/HTTPS listener definitions. The field is required and case sensitive. It does **NOT** support embedded dynamic syntax (`"[a\|b\|c]"`).                                                                                                                                 |
| uri       | • Applies to **profile.http-get.uri** and **profile.http-post.uri**.<br><br>• Resolved URI Length:<br>   ◦ Get Max Length = 127<br>   ◦ Post Max Length = 64<br><br>• Optional, but when specified, it cannot resolve to a blank value.<br>   ◦ NOT ALLOWED: `[/aaa]/bbb[\|]`<br><br>• Must start with `/`.<br><br>• Must resolve to valid HTTP URI syntax.                           |
| parameter | • Applies to **profile.http-get.uri** and **profile.http-post.uri**.<br><br>• Up to 10 parameters in a single Host Profile get/post definition.<br><br>• Supports embedded dynamic data syntax in the name and value.<br><br>• If/when the name resolves to a blank value, the parameter will be dropped.<br><br>• Blank parameter values are supported.                              |
| header    | • Applies to **profile.http-get.uri** and **profile.http-post.uri**.<br><br>• Up to 10 headers in a single Host Profile get/post definition.<br><br>• Supports embedded dynamic data syntax in the name and value.<br><br>• If/when the name resolves to a blank value, the header will be dropped.<br><br>• If/when the value resolves to a blank value, the header will be dropped. |

> The header and parameter fields above allow host name specific configuration in addition to the headers and parameters described in the Profile Language/Headers and Parameters section in the guide.

## Restrictions

- Up to 8 host profiles used per listener/beacon
- 1024 byte limit on space for all profiles used in a beacon (use small simple definitions if possible)
- Maximum tokens in a dynamic field: 32

## Host Profile Linting:

- The linting process DOES NOT include Host Profile settings in the default/variant profile sample data it generates. The process does not know which hosts will be assigned to which listeners and which listeners will be assigned to the default or various profile variants to generate the examples.
- The linting process includes several checks for the defined host profiles.
- The Host Profile get/post URI’s must resolve to unique URI’s to identify HTTP requests appropriately. The linting feature will test for possible URI collisions. Linting does not know which profile variants might use specific host profiles, so the linting process checks for duplicates in a larger scope (all variants) than may be actually required.
- Linting requires the process resolve every potential URI, and header/parameter name. Complex dynamic data can result in very large sets of results, which will impact performance and memory.
