import logging

from .service import Service

log = logging.getLogger(__name__)


def create_proxy(service, source, project):
    service_dict = {'image': 'anchal/vaurien',
                    'name': source + service.name,
                    'command': 'vaurien --http --http-port 2020 --protocol redis --proxy 0.0.0.0:6379 --backend '+service.name +':6379 --behavior 50:delay',
                    }
    new_service = Service(client=service.client,
                          project=service.project,
                          links=[(service, None)],
                          **service_dict)
    project.services.append(new_service)
    return new_service

def proxy_links(source, links, project):
    new_links = []
    f = open('/tmp/.monkey', 'w')
    for link in links:
        old_service, alias = link
        f.write(source + ':' + old_service.name + '\n') # format {$SOURCE:$DEST}
        service = create_proxy(old_service, source, project)
        new_links.append((service, alias or old_service.name))

    f.close()
    return new_links
