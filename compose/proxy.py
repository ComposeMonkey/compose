import logging

from .service import Service

log = logging.getLogger(__name__)

def create_ui(project, client, name):
    service_dict = {'image': 'prat0318/flask_monkey',
                    'name': 'composemonkey',
                    }
    new_service = Service(client=client, project=name, **service_dict)
    project.services.append(new_service)
    return new_service

def create_proxy(service, source, project):
    service_dict = {'image': 'anchal/vaurien',
                    'name': source + service.name,
                    'command': 'vaurien',
                    'source': source
                    }
    new_service = Service(client=service.client,
                          project=service.project,
                          links=[(service, None)],
                          **service_dict)
    project.services.append(new_service)
    return new_service

def proxy_links(source, links, project, name, composemonkey):
    new_links = []
    for link in links:
        old_service, alias = link
        service = create_proxy(old_service, source, project)
        new_links.append((service, alias or old_service.name))
        composemonkey.links.append(
            (service, 'composemonkey_{0}_{1}'.format(source, old_service.name)))
            # (service, None))

    return new_links
