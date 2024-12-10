def format(classess_with_comments, properties_with_comments, base_namespace, namespace_prefix):
    classess = _extract(classess_with_comments, base_namespace, namespace_prefix)
    properties = _extract(properties_with_comments, base_namespace, namespace_prefix)
    
    return f"Classess:\n{classess}\nProperties:\n{properties}"

def _extract(objects_with_comments, base_namespace, namespace_prefix):
    old = base_namespace + "#"
    new = namespace_prefix + ":"
    return "\n".join([f"- {str(o).replace(old, new)}: {com}" for o, com in objects_with_comments])

def format_classess(classess_with_comments, base_namespace, namespace_prefix):
    return _extract(classess_with_comments, base_namespace, namespace_prefix)

def format_properties(properties_with_comments, base_namespace, namespace_prefix):
    return _extract(properties_with_comments, base_namespace, namespace_prefix)
