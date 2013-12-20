${request.dataset.formatted_editors()|n} ${request.dataset.published.year if request.dataset.published else request.dataset.updated.year}.
The ${request.dataset.name} Database.
${request.dataset.publisher_place}: ${request.dataset.publisher_name}.
(Available online at http://${request.dataset.domain}, Accessed on ${h.datetime.date.today()}.)
