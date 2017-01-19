try:
        servers={{ groups['osb_managed'] }}
        port={{ ms_port }}
        j=1
        readDomain("{{ aserver_path }}")
        #print 'Configuring cluster ' + '{{ cluster_name }}' + '...'
        #cd('/')
        #cluster = create('{{ cluster_name }}', 'Cluster')
        #cluster.setClusterMessagingMode('unicast')
        #cluster.setFrontendHost('{{ cluster_address }}')
        #cluster.setFrontendHTTPPort(int('{{ cluster_port }}'))
        #cluster.setClusterAddress('{{ cluster_address }}')
        #cluster.setTxnAffinityEnabled(true)
        #print 'Configured cluster ' + '{{ cluster_name }}' + '\n'
        for i in servers :
                server_name='OSB_MS' + str(j)
                cd('/')
                if server_name == 'OSB_MS1' :
                        cd('/Servers/osb_server1')
                        cmo.setName('OSB_MS1')
                else :
                        create(server_name,'Server')
                        cd('/Servers/' + server_name)
                cmo.setListenAddress(i)
                cmo.setListenPort(port)
                set('Machine',i)
                setServerGroups(server_name,["OSB-MGD-SVRS-COMBINED"])
                print 'Added ' + server_name + ' to this domain'
                #assign('Server',server_name,'Cluster','{{ cluster_name }}')
                #print 'Added ' + server_name + ' to ' + '{{ cluster_name }}'
                j=j+1
        updateDomain()
except Exception,e:
        print str(e)
        print 'Failed while creating managed servers'
