import json
import os
import re
import textwrap
from jinja2 import Environment, FileSystemLoader

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------

import re, textwrap

def _extract_params(path: str) -> list[str]:
    """/teams/<int:id>  ->  id      |  /players/country/<string:country> -> country"""
    m = re.findall(r'<[^:]+:([^>]+)>', path)
    return ", ".join(m)                      # mehrere Parameter möglich

def _handler_name(path: str) -> str:
    cleaned = re.sub(r'[<>/:]', '_', path).strip('_')
    return cleaned.replace('__', '_')

def _make_branch(method: str, ep: dict) -> str:
    mdl = ep["model"]
    path = ep["path"]
    get_List = ep["get_List"]
    params = _extract_params(path)           # z.B. ['team_id'] oder ['name']
    segments = path.strip('/').split('/')    # z.B. ['teams','<int:team_id>','players']
    code = ""

    # 1) Nested Resource?
    #   /teams/<int:team_id>/players
    if len(segments) >= 3 and segments[-2].startswith('<'):
        parent_seg = segments[-3]               # 'teams'
        child_seg  = segments[-1]               # 'players'
        ParentModel = parent_seg[:-1].capitalize()  # 'Team'
        if method == "GET":
            code = f"""
                parent = {ParentModel}.query.get({params})
                if not parent:
                    return jsonify({{"message": "{ParentModel} not found"}}), 404
                children = parent.{child_seg}
                return jsonify([c.to_dict() for c in children])
            """
        elif method == "POST":
            code = f"""
                data = request.get_json()
                data['{params}'] = {params}
                new_obj = {mdl}(**data)
                db.session.add(new_obj)
                db.session.commit()
                return jsonify(new_obj.to_dict()), 201
            """

    # 2) Search or Filter Endpoint?
    #   /players/name/<string:name> or /players/country/<string:country>
    if len(segments) == 2 and segments[-2].startswith('<'):
        val = params
        if get_List:
            code = f"""
                objs = {mdl}.query.filter_by(**{{"{params}": val}}).all()
                if not objs:
                    return jsonify({{"message": "{mdl} not found"}}), 404
                return jsonify([o.to_dict() for o in objs])
            """
        else:
            code = f"""
                obj = {mdl}.query.filter_by(**{{"{params}": val}}).first()
                if not obj:
                    return jsonify({{"message": "{mdl} not found"}}), 404
                return jsonify(obj.to_dict())
            """

    # 3) Standard CRUD
    else:
        if method == "POST":
            code = f"""
                data = request.get_json()
                new_obj = {mdl}(**data)
                db.session.add(new_obj)
                db.session.commit()
                return jsonify(new_obj.to_dict()), 201
            """
        elif method == "GET":
            if params:  # Detail‑GET
                code = f"""
                    obj = {mdl}.query.get({params})
                    if not obj:
                        return jsonify({{"message": "{mdl} not found"}}), 404
                    return jsonify(obj.to_dict())
                """
            else:       # List‑GET
                code = f"""
                    objs = {mdl}.query.all()
                    return jsonify([o.to_dict() for o in objs])
                """
        elif method == "PUT":
            code = f"""
                obj = {mdl}.query.get({params})
                if not obj:
                    return jsonify({{"message": "{mdl} not found"}}), 404
                data = request.get_json()
                for k, v in data.items():
                    setattr(obj, k, v)
                db.session.commit()
                return jsonify(obj.to_dict())
            """
        elif method == "DELETE":
            code = f"""
                obj = {mdl}.query.get({params})
                if not obj:
                    return jsonify({{"message": "{mdl} not found"}}), 404
                db.session.delete(obj)
                db.session.commit()
                return jsonify({{"message": "{mdl} deleted"}})
            """

    # Einrücken
    return textwrap.dedent(code).strip()



def _enrich_endpoints(data: dict):
    model_names = ", ".join({ep["model"] for ep in data["endpoints"]})
    data["models_import"] = model_names
    for ep in data["endpoints"]:
        ep["handler_name"] = _handler_name(ep["path"])
        ep["params"]       = _extract_params(ep["path"])
        # Branches dict: {"GET": "...", "POST": "...", ...}
        ep["branches"] = {m: _make_branch(m, ep) for m in ep["methods"]}

# ------------------------------------------------------------

def enrich_Endpoints(context: dict):
    # --- ENRICH ENDPOINTS -----------------------------------
    if "endpoints" in context:
        _enrich_endpoints(context)
        # Write the enriched context to a JSON file
        output_path = "Output/backendCrew/routes_Enriched.json"
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(context, json_file, indent=4)
        return context

def renderTemplate(template: str, context_file: str, output_file: str):
    with open(context_file, "r", encoding="utf-8") as f:
        context = json.load(f)

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

# Temp Main for testing
if __name__ == '__main__':
    print("Render templates")
    # --- READ JSON FILES -----------------------------------
    with open("Output/backendCrew/models.json", "r", encoding="utf-8") as f:
        models = json.load(f)
    
    with open("Output/backendCrew/routes.json", "r", encoding="utf-8") as f:
        routes = json.load(f)

    # --- RENDER TEMPLATES ----------------------------------
    renderTemplate("models.j2", models, "Output/models.py")
    renderTemplate("app.j2", routes, "Output/app.py")