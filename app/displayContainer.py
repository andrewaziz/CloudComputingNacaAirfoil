import swiftclient.client
import os
import cloudfiles
 
conf = {'user':os.environ['OS_USERNAME'],
        'key':os.environ['OS_PASSWORD'],
        'tenant_name':os.environ['OS_TENANT_NAME'],
        'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=2, **conf)


def getContainerxml(containerName):
    filesxml = []
    filesm = []
    files = []
    missingfilesxml = []
    for data in conn.get_container(containerName)[1]:
        if('{0}'.format(data['name']).endswith(".xml")):
            filesxml.append('{0}'.format(data['name']))
        elif ('{0}'.format(data['name']).endswith(".m")):
            filesm.append('{0}'.format(data['name']))
    for filem in filesm:
        for filexml in filesxml:
            if filem.startswith(filexml):
                if filexml not in files:
                    files.append(filexml)
                    files.append(filem)

        
    return files
    

def displayTable(files):
    html = '<h2>"Currently computed files"</h2>\n<table style="width:100%">\n'
    for i in xrange (0, len(files), 2):
        html += '<tr>\n' + '<td>' + files[i] + '</td>\n'
        html += '<td>' + files[i+1] + '</td>\n'
    html +=  '</table>'
    return html

f = getContainerxml("g17container")
a = displayTable(f)
print a
