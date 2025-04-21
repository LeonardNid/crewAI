import json
import os
import re
import textwrap
from jinja2 import Environment, FileSystemLoader

def cleanup_quotes_in_file(file_path: str):
    """
    Reads the file, strips away any leading/trailing quotes or triple quotes 
    if they wrap the entire file, and then rewrites the cleaned content.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Trim whitespace at start/end
    stripped_content = content.strip()

    # Potential quote fences to remove if they wrap the entire file
    fences = ['"""', "'''", "```", '"', "'"]

    # Try each fence in turn. If the file starts & ends with the same fence, remove them.
    for fence in fences:
        if stripped_content.startswith(fence) and stripped_content.endswith(fence):
            # Remove the leading/trailing fence
            stripped_content = stripped_content[len(fence):-len(fence)].strip()
            # After removing one matching fence pair, break or it might re-check 
            # with single quotes, etc.
            break
    
    if stripped_content.lower().startswith("python"):
        stripped_content = stripped_content[len("python"):].lstrip("\n").lstrip()
    
    # Write back the cleaned content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(stripped_content)

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------
import re, textwrap

def extract_params(path: str) -> str:
    """/teams/<int:id>  ->  id      |  /players/country/<string:country> -> country"""
    m = re.findall(r'<[^:]+:([^>]+)>', path)
    return ", ".join(m)                      # mehrere Parameter möglich

def handler_name(path: str) -> str:
    """/teams/<int:id>/players  ->  teams_id_players"""
    cleaned = re.sub(r'[<>/:]', '_', path).strip('_')
    return cleaned.replace('__', '_')

def make_branch(method: str, ep: dict) -> str:
    mdl = ep["model"]
    if method == "POST":
        return f"""        data = request.get_json()
new_obj = {mdl}(**data)
db.session.add(new_obj)
db.session.commit()
return jsonify(new_obj.to_dict()), 201"""

    if method == "GET":
        if "<" in ep["path"]:        # Detail‑Abruf
            pk = extract_params(ep["path"]) or "id"
            return f"""        obj = {mdl}.query.get({pk})
if not obj:
    return jsonify({{"message": "{mdl} not found"}}), 404
return jsonify(obj.to_dict())"""
        else:                        # Liste
            return f"""        objs = {mdl}.query.all()
return jsonify([o.to_dict() for o in objs])"""

    if method == "PUT":
        return f"""        obj = {mdl}.query.get(id)
if not obj:
    return jsonify({{"message": "{mdl} not found"}}), 404
data = request.get_json()
for k, v in data.items():
    setattr(obj, k, v)
db.session.commit()
return jsonify(obj.to_dict())"""

    if method == "DELETE":
        return f"""        obj = {mdl}.query.get(id)
if not obj:
    return jsonify({{"message": "{mdl} not found"}}), 404
db.session.delete(obj)
db.session.commit()
return jsonify({{"message": "{mdl} deleted"}})"""

    return "pass"   # fallback

def enrich_endpoints(data: dict):
    model_names = ", ".join({ep["model"] for ep in data["endpoints"]})
    data["models_import"] = model_names
    for ep in data["endpoints"]:
        ep["handler_name"] = handler_name(ep["path"])
        ep["params"]       = extract_params(ep["path"])
        # Branches dict: {"GET": "...", "POST": "...", ...}
        ep["branches"] = {m: make_branch(m, ep) for m in ep["methods"]}

# ------------------------------------------------------------

def renderTemplate(template: str, context: dict, output_file: str):
    # --- ENRICH ENDPOINTS -----------------------------------
    if "endpoints" in context:
        enrich_endpoints(context)
        # Write the enriched context to a JSON file
        with open("Output/app_Enriched_JSON.json", "w", encoding="utf-8") as json_file:
            json.dump(context, json_file, indent=4)

    # --- RENDER ---------------------------------------------
    env = Environment(
        loader=FileSystemLoader("files/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl = env.get_template(template)
    rendered = tpl.render(**context)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(rendered)
