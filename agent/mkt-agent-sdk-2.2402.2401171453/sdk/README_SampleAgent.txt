These instructions describe how to build and run the SampleAgent and SampleCMSAgent code. The first section is
the setup instructions.   Section 2 describe how to run the SampleAgent code to retrieve CI360 events from CI360 and
display them.  Section 3 describes how to run the SampleCMSAgent code to integrate CI360 with a third party CMS.
Section 4 describes how to run the SampleMultiAgent code that can connect to multiple CI360 agents.  Section 5 describes
how to connect to CI360 through a proxy server.

Section 1.  Common setup

1. download java 11 higher
2. download maven 3.5.3 or higher from maven.apache.org

3. Add maven bin directory to $PATH or %PATH%
4. set/export JAVA_HOME environment variable to point at java install root directory


5. install CI360 SDK jar into your local repository
	mvn install:install-file -Dfile=<path where CI360 agent was downloaded>/sdk/mkt-agent-sdk-jar-1.<current release>.jar \
	       -DpomFile=<path where CI360 agent was downloaded>/sdk/pom.xml

6. create directory for building the sample agent.
7. copy <path where CI360 agent was downloaded>/sdk/sample/pom.xml to the <sample agent> folder
8. copy <path where CI360 agent was downloaded>/sdk/sample/logback.xml to the <sample agent> folder
9. create src/main/java/sample subfolder under the <sample agent> folder.
10. copy <path where CI360 agent was downloaded>/sdk/sample/*.java to the <sample agent>/src/main/java/sample folder.

11. change directory to the <sample agent> directory that was created.

12. build the sample agents
	mvn compile

13. From the CI360 General Settings:External Access UI, you can get the CI360 Gateway Address to be used in Sections 2, 3 and 4 below.
    The UI displays a full URL (e.g. https://extapigwservice-prod.ci360.sas.com/marketingGateway).
    Be aware that only the host name is used (e.g. extapigwservice-prod.ci360.sas.com).

14. create an agent definition using the CI360 UI. That definition will include a tenant ID and client secret to be used in Sections 2, 3 and 4 below.


Section 2.  Run the SampleAgent to retrieve and display events from CI360

1. run the sample agent from the <sample agent> directory
	mvn exec:java -Dci360.gatewayHost=<CI360 Gateway host> -Dci360.tenantID=<tenant ID> -Dci360.clientSecret=<client secret> \
	        -Dlogback.configurationFile=logback.xml -Dexec.mainClass="sample.SampleAgent" -s "<maven install root directory>\conf\settings.xml"

The agent will output all events configured to be sent to the agent configured in step 13 of Section 1.  In addition, the following commands are available:

	send <external event JSON>
		injects the external event into CI360.

	bulk <application ID>
		requests a signed URL into which a set of events to be injected into Ci360 can be written 

	ping
		indicates whether the CI360 Gateway is available

	healthcheck
		indicates whether the CI360 Gateway is running

    connection
        returns the status of the streaming connection with the gateway
        
	diagnostics
	    returns a detailed status of the CI360 Gateway
		
	sendmessage <message>
		sends a String message to the CI360 Gateway over the websocket
	    
	exit
		exits the sample agent

		
Section 3.   Run the SampleCMSAgent to integrate a 3rd party CMS into CI360.

1. run the sample CMS agent from the <sample agent> directory
	mvn exec:java -Dci360.gatewayHost=<CI360 Gateway host> -Dci360.tenantID=<tenant ID> -Dci360.clientSecret=<client secret> \
	        -Dci360.cmsURL=<URL of the 3rd party CMS> \
	        -Dlogback.configurationFile=logback.xml -Dexec.mainClass="sample.SampleCMSAgent" -s "<maven install root directory>\conf\settings.xml"

The agent will forward all CMS requests from CI360 to the CMS configured in the ci360.cmsURL property.
    From the CI360 UI, you can view the assets stored in the 3rd party CMS.   See the CI360 User's Guide for more information.

These commands are available:
	    
	exit
		exits the sample agent
		


Section 4.  Run the SampleMultiAgent to retrieve events from CI360 for two agents.

1. Create a second agent definition like was done in  Section 1, step 14.

2. run the sample agent from the <sample agent> directory
	mvn exec:java -Dci360.gatewayHost1=<CI360 Gateway host> -Dci360.tenantID1=<first tenant ID> -Dci360.clientSecret1=<first client secret> \
			-Dci360.gatewayHost2=<second CI360 Gateway host> -Dci360.tenantID2=<second tenant ID> -Dci360.clientSecret2=<second client secret> \
	        -Dlogback.configurationFile=logback.xml -Dexec.mainClass="sample.SampleMultiAgent" -s "<maven install root directory>\conf\settings.xml"

The agent should receive and display events for both agents.  The same commands as described in the Section 2 apply.

Section 5. Connecting to the CI360 gateway through a proxy server

The SDK supports connecting to CI360 via a proxy HTTP server.   To use a proxy server, the following options
are used on the mvn command lines in section 2, section 3 and section 4.  The connection to the proxy can be
authenticated or not.

       -Dhttp.proxyHost=<proxy server host name>
       -Dhttp.proxyPort=<port used by proxy server>
       -Dhttp.nonProxyHosts=<list of hosts to which communication does not go through the proxy>
   If authenticated, the following are used
       -Dhttp.proxyUser=<user name on proxy server>
       -Dhttp.proxyPassword=<user password on proxy server>
       -Dhttp.proxyRealm=<the authentication realm for the proxy> 

