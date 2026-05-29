# Mythic for Developers Video Series Notes

Source playlist: `PLJK0fZNGiFU_iJI2A8S5OdloTDexi5zs8` / "Mythic for Developers".

Available playlist topics used to shape this skill:

1. Remote Development
2. Agent Definitions
3. C2 Profile Definitions
4. Translation Containers
5. 3rd Party Service Agents

Captions were not accessible from this environment due YouTube bot/sign-in gating, so this reference uses the playlist topic structure plus official Mythic documentation and local Mythic references. Use this file as routing guidance, not as a transcript.

## Topic-to-skill routing

| Playlist topic | Use this skill/reference |
|---|---|
| Remote Development | `mythic-profiles` -> `profile-development.md` / `remote-development.md` |
| Agent Definitions | `$mythic-implant-development` |
| C2 Profile Definitions | `mythic-profiles` -> `profile-development.md` |
| Translation Containers | `$mythic-translation-containers` |
| 3rd Party Service Agents | `mythic-profiles` when the profile bridges an external service; otherwise create a focused service-agent skill later |

## Practical interpretation

- Keep profile work separate from payload-type work: profile containers describe and run transports; payload types declare profile support and embed selected parameters.
- Translation containers are a separate skill because they are cross-cutting: custom wire formats or crypto affect agents and C2 profiles.
- Third-party service profiles should model rate limits, credentials, message polling, and failure semantics as explicit parameters and validation checks.
