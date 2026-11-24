import base64
import json

token = input("Pega tu JWT: ")
header, payload, signature = token.split(".")

def decode_jwt_section(section):
    section += "=" * (-len(section) % 4)
    decoded = base64.urlsafe_b64decode(section)
    return json.loads(decoded)

print("HEADER:")
print(json.dumps(decode_jwt_section(header), indent=2))

print("\nPAYLOAD:")
print(json.dumps(decode_jwt_section(payload), indent=2))
