# Translation Containers

This page describes how to use translation containers for custom message formats and custom encryption.

Source: https://docs.mythic-c2.net/customizing/payload-type-development/translation-containers

## When You Need a Translation Container

- Your agent uses a binary protocol instead of JSON
- Your agent uses different field names or message structure
- You want to handle encryption yourself (`mythic_encrypts = False`)
- You need a custom key exchange protocol

## Setup

1. Set `translation_container = "myTranslator"` in your PayloadType class
2. Create the container code (Python or Go)
3. Register: `sudo ./mythic-cli add myTranslator`
4. Start: `sudo ./mythic-cli start myTranslator`

The translation container appears as a sub-heading under your payload container in Mythic.

## Architecture

Unlike Payload Types and C2 Profiles (which use RabbitMQ), translation containers use **gRPC** for fast responses.

Three functions are called during message processing:

1. **translate_from_c2_format** - Convert agent's custom format to Mythic JSON
2. **translate_to_c2_format** - Convert Mythic JSON to agent's custom format
3. **generate_encryption_keys** - Generate custom encryption keys at build time

## Message Flow

### Agent -> Mythic (translate_from_c2_format)

```
Agent sends custom message
    → C2 Profile receives it
    → Mythic strips UUID, looks up payload type
    → Finds translation container
    → Calls translate_from_c2_format with:
        {
            "enc_key": null or base64 key,
            "dec_key": null or base64 key,
            "uuid": "uuid from message",
            "profile": "c2 profile name",
            "mythic_encrypts": true/false,
            "type": null or "AES256",
            "message": "base64 of raw message"
        }
    → Translation container returns standard Mythic JSON
    → Mythic processes the JSON normally
```

### Mythic -> Agent (translate_to_c2_format)

```
Mythic generates JSON response
    → Calls translate_to_c2_format
    → Translation container converts to custom format
    → If mythic_encrypts=False:
        Container must encrypt, prepend UUID, base64 encode
        Mythic forwards the result as-is
    → If mythic_encrypts=True:
        Container returns custom bytes only
        Mythic adds UUID and base64 encoding
    → C2 Profile sends to agent
```

## Python Example

```python
from mythic_container.TranslationBase import *

class MyTranslator(TranslationContainer):
    name = "myTranslator"
    description = "Translates between binary protocol and Mythic JSON"
    author = "@you"

    async def translate_from_c2_format(
        self, inputMsg: TrMythicC2ToCustomMessageFormatMessage
    ) -> TrMythicC2ToCustomMessageFormatMessageResponse:
        response = TrMythicC2ToCustomMessageFormatMessageResponse(Success=True)
        # inputMsg.Message contains base64 of the raw message
        # inputMsg.UUID, inputMsg.MythicEncrypts, inputMsg.CryptoKeys
        # Parse your custom format and return standard Mythic JSON
        response.Message = standard_mythic_json_bytes
        return response

    async def translate_to_c2_format(
        self, inputMsg: TrCustomMessageToMythicC2FormatMessage
    ) -> TrCustomMessageToMythicC2FormatMessageResponse:
        response = TrCustomMessageToMythicC2FormatMessageResponse(Success=True)
        # inputMsg.Message contains the Mythic JSON bytes
        # Convert to your custom format
        response.Message = custom_format_bytes
        return response

    async def generate_encryption_keys(
        self, inputMsg: TrGenerateEncryptionKeysMessage
    ) -> TrGenerateEncryptionKeysMessageResponse:
        response = TrGenerateEncryptionKeysMessageResponse(Success=True)
        response.EncryptionKey = generated_enc_key_bytes
        response.DecryptionKey = generated_dec_key_bytes
        return response
```

## GoLang Example

```go
package translationfunctions

import (
    translationstructs "github.com/MythicMeta/MythicContainer/translation_structs"
)

var myTranslation = translationstructs.TranslationContainer{
    Name:        "myTranslator",
    Description: "Custom binary protocol translator",
    Author:      "@you",
}

func fromC2Format(input translationstructs.TrMythicC2ToCustomMessageFormatMessage) translationstructs.TrMythicC2ToCustomMessageFormatMessageResponse {
    // Convert from custom format to Mythic JSON
    return translationstructs.TrMythicC2ToCustomMessageFormatMessageResponse{
        Success: true,
        Message: mythicJsonBytes,
    }
}

func toC2Format(input translationstructs.TrCustomMessageToMythicC2FormatMessage) translationstructs.TrCustomMessageToMythicC2FormatMessageResponse {
    // Convert from Mythic JSON to custom format
    return translationstructs.TrCustomMessageToMythicC2FormatMessageResponse{
        Success: true,
        Message: customFormatBytes,
    }
}

func Initialize() {
    translationstructs.AllTranslationData.Get("myTranslator").AddTranslationDefinition(myTranslation)
    translationstructs.AllTranslationData.Get("myTranslator").AddFromC2FormatFunction(fromC2Format)
    translationstructs.AllTranslationData.Get("myTranslator").AddToC2FormatFunction(toC2Format)
}
```

## Custom EKE via Translation Container

For custom key exchange, return `staging_translation` instead of `checkin`:

```json
{
    "action": "staging_translation",
    "session_id": "random session id",
    "enc_key": "<raw bytes of enc key for next message>",
    "dec_key": "<raw bytes of dec key for next message>",
    "crypto_type": "your_crypto_identifier",
    "next_uuid": "UUID for next message",
    "message": "<raw bytes to send back to agent>"
}
```

This repeats until you finally return a `checkin` action.

### Persistent Storage Between Staging Messages

- `create_agentstorage(unique_id, data)` - Store arbitrary bytes
- `get_agentstorage(unique_id)` - Retrieve stored data
- `delete_agentstorage(unique_id)` - Clean up

## Important Notes

- Docker container names cannot have capital letters
- If `mythic_encrypts = False` and your translation container handles crypto, then on the `translate_to_c2_format` response, Mythic does NOTHING with the message - your container must encrypt, prepend UUID, and base64 encode.
- If `mythic_encrypts = True`, return only the custom bytes and Mythic handles UUID and base64.
- A translation container can be turned from a VM instead of Docker, following the same process as payload type containers.
