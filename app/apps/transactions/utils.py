def filter_response_fields(model, request):
    """Checks if request params has fields key and returns an array of fields.
    """

    fields = None
    compulsory_fields = {"id"}
    if ("fields" in request.GET) and (request.GET["fields"]):
        fields = request.GET["fields"].split(",")
        fields = list(compulsory_fields.union(set(fields)))
        
    return fields