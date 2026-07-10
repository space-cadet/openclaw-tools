# pass-secrets — Password Store Skill

Store and retrieve secrets using `pass` (password-store) with GPG encryption.

## Setup

```bash
# Initialize pass with your GPG key:
# - GPG key: <YOUR_GPG_KEY_ID>
# - Pass store: ~/.password-store/
```

## Usage

### Store a secret
```bash
pass insert -m path/to/secret
# Type value, press Ctrl+D
```

Or pipe directly:
```bash
echo "value" | gpg --encrypt --recipient <YOUR_GPG_KEY_ID> > ~/.password-store/path.gpg
```

### Retrieve a secret
```bash
pass show path/to/secret
```

### List all secrets
```bash
pass ls
```

### Remove a secret
```bash
pass rm path/to/secret
```

## Example Secret Paths

| Path | Description |
|------|-------------|
| `api/service-name` | API key for a service |
| `api/another-service` | Another API key |

Replace with your own secret paths as needed.

## Security

- Secrets are GPG-encrypted at rest
- Only the holder of the private key can decrypt
- Back up `~/.password-store/` and `~/.gnupg/` separately
