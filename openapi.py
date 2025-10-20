import json
import subprocess
from pathlib import Path
from api.adapters.rest.server import app

def generate_openapi_spec():
    root_dir = Path(__file__).parent
    openapi_schema = app.openapi()
    output_file = root_dir / "openapi.json"
    with open(output_file, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    
    subprocess.run([
        "npx", "@hey-api/openapi-ts",
        "-i", "openapi.json",
        "-o", "app/src/lib"
    ], cwd=root_dir)
    
    return output_file

if __name__ == "__main__":
    generate_openapi_spec()
