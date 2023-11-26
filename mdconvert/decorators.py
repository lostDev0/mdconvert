def typer_member_command(typer):
    def actual_decorator(f):
         typer.command()(f)
         return f
    return actual_decorator