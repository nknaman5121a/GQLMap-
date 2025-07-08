# core/schema_enum.py

import httpx
import json

INTROSPECTION_QUERY = {
    "query": """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        types {
          ...FullType
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      fields(includeDeprecated: true) {
        name
        args {
          name
          type {
            name
            kind
            ofType {
              name
              kind
            }
          }
        }
        type {
          name
          kind
          ofType {
            name
            kind
          }
        }
      }
    }
    """
}

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def test_introspection(url):
    try:
        response = httpx.post(url, json=INTROSPECTION_QUERY, headers=HEADERS, timeout=10)
        if "__schema" in response.text:
            return True, response.json()
        else:
            return False, None
    except Exception as e:
        return False, None

def save_schema(schema_data, output_file="output/schema.json"):
    try:
        with open(output_file, "w") as f:
            json.dump(schema_data, f, indent=2)
        print(f"[+] Schema saved to {output_file}")
    except Exception as e:
        print(f"[!] Failed to save schema: {e}")
