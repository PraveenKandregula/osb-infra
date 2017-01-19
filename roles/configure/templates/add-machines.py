try:
        servers={{ groups['osb_managed'] }}
        print 'Adding machines to domain...\n'
        readDomain("{{ aserver_path }}")
        for i in servers :
                cd('/')
                #cmo.createUnixMachine(i)
                create(i,'UnixMachine')
                cd('/UnixMachines/'+i)
                nmgr = create(i,'NodeManager')
                nmgr.setNMType('Plain')
                nmgr.setListenAddress(i)
                nmgr.setListenPort({{ nm_port }})
                nmgr.setDebugEnabled(false)
                print 'Added machine:' + i + ' to domain'
	updateDomain()
        setServerGroups('AdminServer',["WSM-CACHE-SVR" , "WSMPM-MAN-SVR" , "JRF-MAN-SVR"])
	cd('/SecurityConfiguration/'+"{{ domain_name }}")
	cmo.setNodeManagerUsername("{{ weblogic_username }}")
	cmo.setNodeManagerPasswordEncrypted("{{ weblogic_password }}")
	set('CrossDomainSecurityEnabled',true)
	updateDomain()
        print '\nAdded machines to domain'
except Exception,e:
        print str(e)
        dumpStack()
        print 'Failed at adding machine to domain'
