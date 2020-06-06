from textx import get_children, get_parent_of_type, TextXSemanticError


def variable_scope_check(model, metamodel):
    def _decl_decider(x):
        return (
            hasattr(x, "name") and x.name is not None
            and (x.name.startswith("?") or x.name.startswith("!"))
            and (
                get_parent_of_type("Formula", x) is None
                and get_parent_of_type("ClassPatternDecl", x) is None
                and get_parent_of_type("PropertyPatternDecl", x) is None
                and get_parent_of_type("AttributePatternDecl", x) is None
                and get_parent_of_type("DatatypePatternDecl", x) is None
                and get_parent_of_type("IndividualPatternDecl", x) is None
                and get_parent_of_type("PropertyRestrictionPatternDecl", x) is None
                and get_parent_of_type("AttributeRestrictionPatternDecl", x) is None
                and get_parent_of_type("ModalPatternDecl", x) is None
                and get_parent_of_type("LiteralPatternDecl", x) is None
            )
        )

    def _ref_decider(x):
        return (
            ((hasattr(x, "universal_var") and x.universal_var is not None) or (hasattr(x, "existential_var") and x.existential_var is not None))
            and (
                get_parent_of_type("Formula", x) is None
                and get_parent_of_type("ClassPatternDecl", x) is None
                and get_parent_of_type("PropertyPatternDecl", x) is None
                and get_parent_of_type("AttributePatternDecl", x) is None
                and get_parent_of_type("DatatypePatternDecl", x) is None
                and get_parent_of_type("IndividualPatternDecl", x) is None
                and get_parent_of_type("PropertyRestrictionPatternDecl", x) is None
                and get_parent_of_type("AttributeRestrictionPatternDecl", x) is None
                and get_parent_of_type("ModalPatternDecl", x) is None
                and get_parent_of_type("LiteralPatternDecl", x) is None
            )
        )

    def _headed_list_decider(x):
        return (
            (x.__class__.__name__ == "HeadedList" or x.__class__.__name__.startswith("Infix"))
            and (
                get_parent_of_type("Formula", x) is None
                and get_parent_of_type("ClassPatternDecl", x) is None
                and get_parent_of_type("PropertyPatternDecl", x) is None
                and get_parent_of_type("AttributePatternDecl", x) is None
                and get_parent_of_type("DatatypePatternDecl", x) is None
                and get_parent_of_type("IndividualPatternDecl", x) is None
                and get_parent_of_type("PropertyRestrictionPatternDecl", x) is None
                and get_parent_of_type("AttributeRestrictionPatternDecl", x) is None
                and get_parent_of_type("ModalPatternDecl", x) is None
                and get_parent_of_type("LiteralPatternDecl", x) is None
            )
        )

    issues = get_children(_decl_decider, model)
    issues += get_children(_ref_decider, model)
    issues += get_children(_headed_list_decider, model)
    if len(issues) > 0:
        first_error = issues[0]
        if hasattr(first_error, "name"):
            var = "Variable '{}'".format(first_error.name)
        elif hasattr(first_error, "universal_var"):
            var = "Variable '{}'".format(first_error.universal_var)
        elif hasattr(first_error, "existential_var"):
            var = "Variable '{}'".format(first_error.existential_var)
        elif hasattr(first_error, "head"):
            var = "Headed list '{}'".format(first_error.head.ref.name)
        else:
            var = "Infix expression '{}'".format(first_error)
        parser = model._tx_parser
        line, col = parser.pos_to_linecol(
            first_error._tx_position
            )
        message = "{} used outside a formula or pattern in '{}'".format(
            var,
            str(first_error)
            )
        raise TextXSemanticError(
            message,
            line=line,
            col=col,
            filename=model._tx_filename
            )


def temporal_recursion_checker(model, metamodel):
    def _decider(x):
        return (x.__class__.__name__ == "ClassExpressionRecursion"
                and get_parent_of_type("ClassExpressionModalRepeat", x)
                is None)
    issues = get_children(_decider, model)
    if len(issues) > 0:
        first_error = issues[0]
        parser = model._tx_parser
        line, col = parser.pos_to_linecol(
            first_error._tx_position
            )
        message = "'again' used outside a recursion '{}'".format(
            str(first_error)
            )
        raise TextXSemanticError(
            message,
            line=line,
            col=col,
            filename=model._tx_filename
            )