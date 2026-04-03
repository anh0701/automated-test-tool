from copy import error


def validate_check_request(request):

    if "spec" in request.files and "vectors" in request.files:
        try:
            import json

            spec_file = request.files["spec"]
            vector_file = request.files["vectors"]

            spec = json.load(spec_file)
            test_vectors = json.load(vector_file)

        except Exception as e:
            return None, None, error(f"Invalid JSON file: {str(e)}")

    elif request.is_json:
        data = request.get_json()
        spec = data.get("spec")
        test_vectors = data.get("test_vectors")

    else:
        return None, None, error("Unsupported input type")

    if not spec:
        return None, None, error("Missing spec")

    if not test_vectors:
        return None, None, error("Missing test_vectors")

    return spec, test_vectors, None