from flask import request, render_template, abort


def object_list(template_name, qr, var_name='object_list', **kwargs):
    paginate_by = 25
    if 'paginate_by' in kwargs:
        paginate_by = kwargs['paginate_by']
    kwargs.update(
        page=int(request.args.get('page', 1)),
        pages=int(qr.count() / paginate_by + 1))
    kwargs[var_name] = qr.paginate(kwargs['page'])
    return render_template(template_name, **kwargs)


def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        abort(404)
