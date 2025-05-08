# Utils.py  –  zentrale Hilfsfunktionen
# -------------------------------------
import json
import os
import re
import textwrap
from typing import Dict, Any, List

from jinja2 import Environment, FileSystemLoader

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ──────────────────────────────────────────────────────────────────────────────
#  ROUTE-HILFSFUNKTIONEN
# ──────────────────────────────────────────────────────────────────────────────
def _extract_params(path: str) -> str:
    """/teams/<int:id> → 'id'   |   /players/country/<string:country> → 'country'"""
    return ", ".join(re.findall(r'<[^:]+:([^>]+)>', path))


def _handler_name(path: str) -> str:
    cleaned = re.sub(r'[<>/:]', '_', path).strip('_')
    return cleaned.replace('__', '_')


def _make_branch(method: str, ep: dict) -> str:
    """Erzeugt den Funktions-Body für einen HTTP-Branch (analog zu bisher)."""
    mdl      = ep["model"]
    path     = ep["path"]
    params   = _extract_params(path)
    segments = path.strip('/').split('/')
    code     = ""

    # 1) Nested Resource  …/teams/<int:team_id>/players
    if len(segments) >= 3 and segments[-2].startswith('<'):
        parent_seg   = segments[-3]
        child_seg    = segments[-1]
        ParentModel  = parent_seg[:-1].capitalize()

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

    # 2) Search / Filter-ähnlicher Endpoint
    #    Beispiel: /players/name/<string:name>
    #              /players/country/<string:country>
    elif (
        len(segments) >= 3                       # genug Segmente
        and segments[-1].startswith('<')         # Platzhalter ganz hinten
        and not segments[-2].startswith('<')     # davor echtes Feld
    ):
        field = segments[-2]                     # z. B. 'name' oder 'country'

        if ep.get("get_List"):                   # Liste zurückgeben
            code = f"""
                objs = {mdl}.query.filter_by(**{{"{field}": {params}}}).all()
                if not objs:
                    return jsonify({{"message": "{mdl} not found"}}), 404
                return jsonify([o.to_dict() for o in objs])
            """
        else:                                    # Einzel-Objekt
            code = f"""
                obj = {mdl}.query.filter_by(**{{"{field}": {params}}}).first()
                if not obj:
                    return jsonify({{"message": "{mdl} not found"}}), 404
                return jsonify(obj.to_dict())
            """

    # 4) Standard CRUD
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
            if params:
                code = f"""
                    obj = {mdl}.query.get({params})
                    if not obj:
                        return jsonify({{"message": "{mdl} not found"}}), 404
                    return jsonify(obj.to_dict())
                """
            else:
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

    return textwrap.dedent(code).strip()


# ──────────────────────────────────────────────────────────────────────────────
#  RELATIONSHIP-HILFSFUNKTIONEN
# ──────────────────────────────────────────────────────────────────────────────
def _relationship_line(model_name: str, rel: Dict[str, Any]) -> str:
    """Erzeugt eine vollständige db.relationship-Zeile - gleicher Stil wie _make_branch."""
    target   = rel["target_model"]
    rel_type = rel["rel_type"].replace("-", "_")
    cascade  = rel["cascade"]

    code = ""

    if rel_type == "one_to_many":
        attr_name = f"{target.lower()}s"
        cascade = "" if cascade is None else f"cascade=\"{cascade}\""
        code = f"""
            {attr_name} = db.relationship(
            '{target}',
            back_populates='{model_name.lower()}',
            lazy=True,
            {cascade}
            )
        """

    elif rel_type == "many_to_one":
        attr_name = target.lower()
        code = f"""
            {attr_name} = db.relationship(
                '{target}',
                back_populates='{model_name.lower()}s',
                lazy=True
            )
        """

    elif rel_type == "many_to_many":
        attr_name     = f"{target.lower()}s"
        assoc_table   = f"{model_name.lower()}_{target.lower()}"
        br            = f"{model_name.lower()}s"
        code = f"""
            {attr_name} = db.relationship(
            '{target}',
            secondary='{assoc_table}',
            backref='{br}',
            lazy='dynamic'
            )
        """
    elif rel_type == "one_to_one":
        attr_name = target.lower()
        code = f"""
            {attr_name} = db.relationship(
            '{target}',
            uselist=False,
            back_populates='{model_name.lower()}',
            lazy=True
            )
        """
    else:
        code = "ERROR: Unsupported rel_type: {rel_type}"

    return textwrap.dedent(code).strip()


# ──────────────────────────────────────────────────────────────────────────────
#  ENRICH-FUNKTIONEN
# ──────────────────────────────────────────────────────────────────────────────
def enrich_Endpoints(context: dict):
    """Bereitet routes.json für Jinja vor (Handler-Namen, Branch-Code …)."""
    if "endpoints" not in context:
        return context

    with open("Output/backendCrew/models.json", "r", encoding="utf-8") as f:
        models_data = json.load(f)
    context["models_import"] = ", ".join(mdl["name"] for mdl in models_data["models"])

    for idx, ep in enumerate(context["endpoints"]):
        ep["idx"]           = idx
        ep["handler_name"] = _handler_name(ep["path"])
        ep["params"]       = _extract_params(ep["path"])
        ep["branches"]     = {m: _make_branch(m, ep) for m in ep["methods"]}

    with open("Output/backendCrew/routes.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=4)
    return context


def enrich_Models(context: Dict[str, Any]):
    """Fügt models.json die vorgerenderten relationship-Strings hinzu."""
    if "models" not in context:
        return context

    for mdl in context["models"]:
        mdl["relationship_lines"] = [
            _relationship_line(mdl["name"], rel)
            for rel in mdl.get("relationships", [])
        ]

    with open("Output/backendCrew/models.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=4)
    return context


# ──────────────────────────────────────────────────────────────────────────────
#  TEMPLATE-RENDERING
# ──────────────────────────────────────────────────────────────────────────────
def renderTemplate(template: str, context_file: str | dict, output_file: str):
    """Rendert eine Jinja-Vorlage mit kontext (Datei- oder Dict-Input)."""
    context = (
        json.load(open(context_file, encoding="utf-8"))
        if isinstance(context_file, str) else context_file
    )

    env = Environment(
        loader=FileSystemLoader("files/templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl       = env.get_template(template)
    rendered  = tpl.render(**context)

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