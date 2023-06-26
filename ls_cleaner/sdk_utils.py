import label_studio_sdk
from typing import Any, Dict, Iterator, List


def get_tasks_iter(
    project: label_studio_sdk.Project,
    filters=None,
    ordering=None,
    view_id=None,
    selected_ids=None,
    only_ids: bool = False,
) -> Iterator[List[Dict[str, Any]]]:
    """ Retrieve a subset of tasks from the Data Manager based on a filter, ordering mechanism, or a
    predefined view ID.

    Parameters
    ----------
    project: label_studio_sdk.Project object
    filters: label_studio_sdk.data_manager.Filters.create()
        JSON objects representing Data Manager filters. Use `label_studio_sdk.data_manager.Filters.create()`
        helper to create it.
        Example:
    ```json
    {
        "conjunction": "and",
        "items": [
        {
            "filter": "filter:tasks:id",
            "operator": "equal",
            "type": "Number",
            "value": 1
        }
        ]
    }
    ```
    ordering: list of label_studio_sdk.data_manager.Column
        List with <b>one</b> string representing Data Manager ordering.
        Use `label_studio_sdk.data_manager.Column` helper class.
        Example:
        ```[Column.total_annotations]```, ```['-' + Column.total_annotations]``` - inverted order
    view_id: int
        View ID, visible as a Data Manager tab, for which to retrieve filters, ordering, and selected items
    selected_ids: list of ints
        Task IDs
    only_ids: bool
        If true, return only task IDs

    Returns
    -------
    list
        Task list with task data, annotations, predictions and other fields from the Data Manager

    """

    page = 1
    while True:
        try:
            data = project.get_paginated_tasks(
                filters=filters,
                ordering=ordering,
                view_id=view_id,
                selected_ids=selected_ids,
                only_ids=only_ids,
                page=page,
                page_size=1000
            )
            yield data['tasks']
            page += 1
        # we'll get 404 from API on empty page
        except label_studio_sdk.project.LabelStudioException:
            break
