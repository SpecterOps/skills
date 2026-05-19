bloginuser

Ask Beacon to create a token from the specified credentials. This is the make_token command. User principle name (UPN) formatting may be used for the username value. In this case, the user's domain value is ignored.

#### Arguments

`$1` - the id for the beacon. This may be an array or a single ID.

`$2` - the domain of the user

`$3` - the user's username

`$4` - the user's password

#### Examples

```
# make a token for a user with an empty password
alias make_token_empty {
   local('$domain $user');
   ($domain, $user) = split("\\\\", $2);
   bloginuser($1, $domain, $user, "");
}

# make a token for a user using UPN syntax
alias make_token_upn_syntax {
   bloginuser($1, "", "user@contoso.corp.com", "password1234");
}```

