readTemplate("{{ wls_template }}")
setOption('ServerStartMode', 'prod')
setOption('DomainName','{{ domain_name }}')
setOption('OverwriteDomain','true')

print 'Configuring Admin server...'
cd('/Servers/AdminServer')
create('AdminServer','SSL')
cd('SSL/AdminServer')
set('Enabled', 'False')
set('HostNameVerificationIgnored', 'True')
cd('/Security/base_domain/User/weblogic')
cmo.setName('{{ weblogic_username }}')
cmo.setUserPassword('{{ weblogic_password }}')
writeDomain("{{ aserver_path }}")
closeTemplate()
print 'Admin server has been configured\n'

readDomain("{{ aserver_path }}")
addTemplate("{{ ws_template }}")
updateDomain()
addTemplate("{{ osb_template }}")

#JDBC
cd('/')
print 'Configuring JDBC...'
jdbcsrcs=cmo.getJDBCSystemResources()
cd('/JDBCSystemResource/LocalSvcTblDataSource/JdbcResource/LocalSvcTblDataSource/JDBCDriverParams/NO_NAME_0')
set('URL','jdbc:oracle:thin:@{{ db_server }}:{{ db_port }}/{{ db_instance }}')
set('PasswordEncrypted','{{ db_schema_password }}')
cd('Properties/NO_NAME_0/Property/user')
set('Value','{{ schema_prefix }}_STB')
getDatabaseDefaults()

for sr in range(len(jdbcsrcs)):
      s = jdbcsrcs[sr]
      cd('/')
      if s.getName() in ["EDNDataSource","wlsbjmsrpDataSource","OraSDPMDataSource","SOADataSource","BamDataSource"]:
        print 'Changing to XA for '+s.getName()
        cd('/JDBCSystemResource/'+s.getName()+'/JdbcResource/'+s.getName()+'/JDBCDriverParams/NO_NAME_0')
        set('DriverName','oracle.jdbc.xa.client.OracleXADataSource')
        set('UseXADataSourceInterface','True')
        cd('/JDBCSystemResource/'+s.getName()+'/JdbcResource/'+s.getName()+'/JDBCDataSourceParams/NO_NAME_0')
        set('GlobalTransactionsProtocol','TwoPhaseCommit')

updateDomain()
print 'JDBC has been configured'
